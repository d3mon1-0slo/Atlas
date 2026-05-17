from core.core import OLLAMA_BASE_URL, OLLAMA_MODEL
from models.model import IdeaInput, IdeaOutput
import httpx
import json
from fastapi import HTTPException
from pydantic import ValidationError

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

class CALL_LLM:

    def __init__(self):
        self.OLLAMA_URL = OLLAMA_BASE_URL
        self.LLM_MODEL = OLLAMA_MODEL
        self.client = httpx.AsyncClient(timeout=60)

    def prompt_builder(self, data):
        valid_types_str = ", ".join(VALID_TYPES)
        prompt = f"""You are a successful techpreneur. Generate exactly 5 startup ideas for your junior based on their profile.

    ## Junior Profile
    - Niche: {data.niche}
    - Details: {data.details}
    - Skill level: {data.skill}/10
    - Background: {data.skill_details}

    ## Task
    Generate 5 startup ideas related to the niche "{data.niche}". The niche is just a THEME — each idea must target a COMPLETELY DIFFERENT type of business or audience.

    For example, if the niche is "Food":
    - Idea 1 -> supermarket (inventory tool)
    - Idea 2 -> restaurant (POS system)
    - Idea 3 -> cafe (loyalty program)
    - Idea 4 -> Remote food delivery platform
    - Idea 5 -> Remote meal planning SaaS

    Never repeat the same business_type or potential_client across ideas.

    ## Steps per idea
    1. Pick a DIFFERENT client type from the previous ideas
    2. Decide if the client is a PHYSICAL local business
    - If YES -> is_local: true, pick business_type from: {valid_types_str}
    - If NO -> is_local: false, business_type: null
    3. Set potential_client:
    - If is_local true -> owner of that business e.g. "Gym Owner", "Cafe Owner", "Pharmacy Owner"
    - If is_local false -> target audience e.g. "Remote Food Startups", "Freelance Nutritionists"

    ## Output Format
    Return ONLY valid JSON, no markdown, no explanation:
    {{
        "ideas": [
            {{"name": "", "description": "", "potential_client": "", "is_local": true, "business_type": "gym"}},
            {{"name": "", "description": "", "potential_client": "", "is_local": false, "business_type": null}}
        ]
    }}

    ## Count Check (verify before outputting)
    - Count your is_local: true ideas -> must be exactly 3
    - Count your is_local: false ideas -> must be exactly 2
    - Count unique business_type values -> must all be different
    - Count unique potential_client values -> must all be different
    - If any check fails, regenerate before outputting
    
    ## Rules
    - Exactly 5 ideas
    - Exactly 3 must have is_local: true with a valid business_type from the list
    - Exactly 2 must have is_local: false with business_type: null
    - Never use the same business_type more than once
    - Never use the same potential_client more than once
    - business_type must be from the valid list, never invent types
    - If is_local is true, business_type MUST NOT be null
    - If is_local is false, business_type MUST be null
    - is_local must be a boolean, never a string
    - JSON only, nothing else
    """
        return prompt

    async def generate_project(self, data: IdeaInput) -> IdeaOutput:
        max_retries = 3

        for attempt in range(max_retries):
            try:
                payload = {
                    "model": self.LLM_MODEL,
                    "prompt": self.prompt_builder(data),
                    "stream": False
                }

                response = await self.client.post(
                    f"{self.OLLAMA_URL}/api/generate",
                    json=payload
                )

                response.raise_for_status()
                res_json = response.json()
                raw_text = res_json.get('response')
                print("RAW:", raw_text) 
                
                parsed = json.loads(raw_text)
                parsed['ideas'] = [
                    idea for idea in parsed.get('ideas', [])
                    if idea.get('name') and idea.get('description')
                ]

                for idea in parsed['ideas']:
                    if idea.get('business_type') and idea['business_type'] not in VALID_TYPES:
                        idea['business_type'] = None
                        idea['is_local'] = False
                validated = IdeaOutput.model_validate(parsed)
                return validated

            except (json.JSONDecodeError, ValidationError, httpx.HTTPStatusError) as e:
                if attempt == max_retries - 1:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error: {str(e)}"
                    )
                continue