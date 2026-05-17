# 🚀 Atlas — AI Startup Idea Validator

> Greek: _καιρός_ — the right or opportune moment. The perfect time to act on an idea.

An AI-powered project idea generator designed to help developers, freelancers, startup founders, and creators discover profitable project ideas based on their skills, niche, and target audience — complete with real nearby local businesses to pitch to.

---

# 🎯 Main Idea

The user inputs:

- Niche / Industry
- Idea details
- Skill level (1–10)
- Skill background

Example:

```txt
Niche:
Healthcare

Idea Details:
I want to build tools that help local clinics manage patients and appointments without expensive enterprise software

Skill Level:
6/10

Skill Background:
Python, FastAPI, PostgreSQL, basic HTML/JS
```

The system then:

1. Sends the data to AI (Ollama / Mistral 7B)
2. AI analyzes the niche and generates 5 tailored startup ideas
3. For local ideas, system fetches real nearby businesses via Google Places API
4. User receives swipeable cards:
   - Swipe Left → Skip
   - Swipe Right → Save

---

# 🧠 Core Features

## 1. AI Project Idea Generator

Generates 5 tailored startup ideas based on:

- Niche / industry theme
- Skill level and background
- Market demand
- Local vs remote opportunity

---

## 2. Local Business Intelligence

If the idea targets a physical local business:

Examples:

- Gyms
- Dental Clinics
- Pharmacies
- Cafes
- Restaurants

The system:

- Detects the business type via LLM mapping
- Fetches real nearby businesses via Google Places API
- Attaches Google Maps links to each business

Example:

```txt
Idea: "Clinic Appointment Scheduler"
→ Nearby businesses: Metro Medical Clinic, City Health Center, Sunrise Clinic
→ Click any pill → Opens directly on Google Maps
```

---

## 3. Swipe-Based UX

Inspired by Tinder-style interactions:

- Swipe left → Skip idea
- Swipe right → Save idea
- Saved ideas appear in a grid on the right
- Click any saved idea → Opens a detail modal with full description and nearby businesses

---

## 4. Smart Type Resolution

The LLM maps freeform niches to valid Google Places API types:

```txt
"coffee shop" → cafe
"clinic"      → doctor, hospital
"law firm"    → lawyer
"agriculture" → hardware_store, store
```

This ensures the Google Places API always receives valid queries and returns relevant results.

---

# 🏗️ Architecture

## Frontend

- HTML
- TailwindCSS (CDN)
- Vanilla JavaScript

### Why?

- Lightweight and fast
- No framework dependency
- Single file — easy to deploy and share

---

## Backend

- FastAPI

### Why FastAPI?

- Modern async Python backend
- AI-engineering friendly
- Clean REST API structure
- Easy integration with Ollama and Google APIs

---

## AI

- Ollama (local inference)
- Model: Mistral 7B

### Why local AI?

- No API costs
- Runs offline
- Full control over the model

---

## Maps & Location

- Google Places API (Nearby Search)
- `geocoder` for IP-based location detection

---

# 🗂️ Project Structure

```
Atlas/
├── core/
│   └── core.py           # env config (API keys, Ollama URL)
├── models/
│   └── model.py          # Pydantic models
├── services/
│   ├── llm.py            # CALL_LLM — idea generation via Ollama
│   └── businesses.py     # GET_BUSINESSES — Google Places integration
├── routers/
│   └── router.py         # FastAPI route definitions
├── main.py               # app entrypoint
├── index.html            # frontend (single file)
├── requirements.txt
└── .env
```

---

# ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/Atlas.git
cd Atlas
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root:

```env
GOOGLE_MAP=your_google_places_api_key
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b
```

### 4. Pull the model and start Ollama

```bash
ollama pull mistral:7b
ollama serve
```

### 5. Run the backend

```bash
uvicorn main:app --reload
```

### 6. Open the frontend

Open `index.html` in your browser.

---

# 📡 API

### `POST /api/v1/generate`

**Request:**

```json
{
  "niche": "Healthcare",
  "details": "I want to build tools that help local clinics manage patients and appointments",
  "skill": 6,
  "skill_details": "Python, FastAPI, PostgreSQL, basic HTML/JS"
}
```

**Response:**

```json
{
  "Response": "Success",
  "Data": {
    "ideas": [
      {
        "name": "Clinic Appointment Scheduler",
        "description": "...",
        "potential_client": "Clinic Owner",
        "is_local": true,
        "business_type": "doctor",
        "local_businesses": [
          {
            "name": "Metro Medical Clinic",
            "type": "doctor",
            "url": "https://www.google.com/maps/place/?q=place_id:ChIJ..."
          }
        ]
      }
    ]
  }
}
```

---

# 📝 Notes

- Location is detected automatically via IP geolocation
- The LLM maps your niche to valid Google Places API types for accurate business search
- Invalid business types returned by the LLM are sanitized on the backend before hitting the API
- Mistral 7B runs locally — no AI API costs
