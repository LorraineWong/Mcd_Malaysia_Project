# 🍔 McDonald's Outlets in Kuala Lumpur, Malaysia

A full-stack app to visualize and search for McDonald’s outlets in Kuala Lumpur.

---

## Features

- Interactive Map with all KL outlets and 5km catchment area
- Outlet info popups (address, features, contact, links)
- Name search with autocomplete and quick focus
- Natural language Chatbot (NLP): e.g. "Which outlets in KL operate 24 hours?"
- Reset map view button

---

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** Vue 3, Vite, Mapbox GL JS
- **Database:** SQLite or PostgreSQL
- **NLP:** Simple rule-based prompt (can upgrade to LLM)

---

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
# Add Mapbox token to .env as VITE_MAPBOX_TOKEN
npm run dev
```

---

## Key Technical Decisions


### Frameworks/Libraries

- **Backend:** FastAPI (easy API creation, async, good docs)
- **Frontend:** Vue 3 + Vite (fast, modern SPA, easy component system)
- **Mapping:** Mapbox GL JS (rich, interactive maps)
- **NLP:** Simple prompt-based extraction (fast to implement, easy control)
- **Database:** SQLite (lightweight, suitable for local/demo use)
    

### Reasoning

- FastAPI + Vue 3 combination allows rapid prototyping and clear separation of frontend/backend.
- Mapbox chosen for beautiful and customizable maps.
- Simple NLP logic for chatbot keeps the app lightweight but easy to extend.
    

### Usage
- View all outlets on the map, with info popups and 5km catchment zones.
- Search by name with autocomplete.
- Use the chatbot for questions (e.g. "Which outlets operate 24 hours?").
- Reset map to default view anytime.
    

### Architecture

**Backend:**
- FastAPI REST API (/outlets, /ask)
- Serves outlet data and responds to chatbot queries
    

**Frontend:**
- Vue SPA, fetches data from API, renders interactive map and UI
    
**Database:**
- SQLite (can upgrade to Postgres if needed)
    
---

## Notes
- All development is local (CORS enabled for demo).
- For production, restrict CORS and use a secure database and API key storage.