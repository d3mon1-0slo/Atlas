from core.core import GOOGLE_MAP, OLLAMA_BASE_URL, OLLAMA_MODEL
from models.model import LocalBusiness
import httpx
import geocoder
from fastapi import HTTPException

VALID_TYPES = [
    "accounting", "airport", "amusement_park", "aquarium", "art_gallery",
    "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store",
    "book_store", "bowling_alley", "bus_station", "cafe", "campground",
    "car_dealer", "car_rental", "car_repair", "car_wash", "casino",
    "cemetery", "church", "city_hall", "clothing_store", "convenience_store",
    "courthouse", "dentist", "department_store", "doctor", "drugstore",
    "electrician", "electronics_store", "embassy", "fire_station", "florist",
    "funeral_home", "furniture_store", "gas_station", "gym", "hair_care",
    "hardware_store", "hindu_temple", "home_goods_store", "hospital",
    "insurance_agency", "jewelry_store", "laundry", "lawyer", "library",
    "light_rail_station", "liquor_store", "local_government_office", "locksmith",
    "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental",
    "movie_theater", "moving_company", "museum", "night_club", "painter",
    "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber",
    "police", "post_office", "primary_school", "real_estate_agency", "restaurant",
    "roofing_contractor", "rv_park", "school", "secondary_school", "shoe_store",
    "shopping_mall", "spa", "stadium", "storage", "store", "subway_station",
    "supermarket", "synagogue", "taxi_stand", "tourist_attraction", "train_station",
    "transit_station", "travel_agency", "university", "veterinary_care", "zoo"
]


class GET_BUSINESSES:

    def __init__(self):
        self.GOOGLE_MAP = GOOGLE_MAP
        self.OLLAMA_URL = OLLAMA_BASE_URL
        self.LLM_MODEL = OLLAMA_MODEL
        self.client = httpx.AsyncClient(timeout=60)

    def get_location(self):
        g = geocoder.ip('me')
        if g.latlng:
            return g.latlng
        return None

    async def resolve_type_via_llm(self, niche: str) -> list[str]:
        print(f"NICHE: {niche}")
        valid_types_str = ", ".join(VALID_TYPES)
        prompt = f"""You are a Google Maps search assistant. Your job is to map a user's business niche to the closest matching Google Places API types.

                Valid Google Places API types:
                {valid_types_str}

                User is searching for businesses in this niche: "{niche}"

                Think about what kind of physical store or place someone in the "{niche}" industry would operate from.
                For example:
                - "agriculture" -> farm supply = hardware_store, store
                - "coffee shop" -> cafe
                - "clinic" -> doctor, hospital
                - "law firm" -> lawyer
                - "school supply" -> book_store, store

                Now match "{niche}" to 1-3 types from the valid list above.
                Return ONLY the matched types, comma-separated, no explanation, no extra text."""

        payload = {
            "model": self.LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }

        response = await self.client.post(
            f"{self.OLLAMA_URL}/api/generate",
            json=payload
        )
        response.raise_for_status()
        raw = response.json().get("response", "").strip()
        print(f"RAW: {raw}")
        matched = [t.strip() for t in raw.split(",") if t.strip() in VALID_TYPES]
        return matched if matched else ["store"]

    async def fetch_by_type(self, lat: float, lon: float, place_type: str) -> list[dict]:
        response = await self.client.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params={
                "location": f"{lat},{lon}",
                "radius": 5000,
                "type": place_type,
                "key": self.GOOGLE_MAP
            }
        )
        data = response.json()
        return data.get("results", [])

    async def get_business(self, niche: str) -> list[LocalBusiness]:
        coords = self.get_location()
        if not coords:
            raise HTTPException(status_code=400, detail="Could not determine location")

        lat, lon = coords

        try:
            place_types = await self.resolve_type_via_llm(niche)

            seen = set()
            businesses = []

            for place_type in place_types:
                results = await self.fetch_by_type(lat, lon, place_type)

                for place in results:
                    name = place.get("name")
                    place_google_types = place.get("types", [])
                    place_id = place.get("place_id")

                    if name in seen:
                        continue
                    if not any(t in place_types for t in place_google_types):
                        continue

                    seen.add(name)
                    businesses.append(LocalBusiness(
                        name=name,
                        type=place_google_types[0] if place_google_types else "unknown",
                        url=f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else None
                    ))

            return businesses

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Maps API error: {str(e)}")