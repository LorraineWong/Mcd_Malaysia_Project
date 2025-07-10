# 🍔 McDonald's Outlets in Kuala Lumpur, Malaysia

A modern full-stack web app to visualize, search, and chat about McDonald’s outlets in Kuala Lumpur.

[Live Demo – Frontend (Vercel)](https://mcd-malaysia-project.vercel.app)  
[Live API (Render)](https://mcd-malaysia-project.onrender.com/docs)

---

## Features

- **Interactive Map**: See all McD outlets in KL with 5km catchment zone
- **Outlet Info Popups**: Address, features, contact, Google/Waze links
- **Fuzzy Search**: Autocomplete outlet names, map quick focus
- **NLP Chatbot**: Ask in natural language, e.g. “Which outlets in KL operate 24 hours?”
- **Responsive UI**: Desktop friendly
- **Reset Map View**: One click to recenter

---

## Tech Stack

| Layer    | Tech & Tools                                         |
|----------|------------------------------------------------------|
| Backend  | Python, FastAPI, Uvicorn                             |
| Frontend | Vue 3, Vite, Mapbox GL JS, Axios                     |
| Database | SQLite (easy demo), PostgreSQL (optional)            |
| NLP      | Simple rule-based extraction (upgradeable to LLM)    |
| Deploy   | Render (API), Vercel (Frontend SPA)                  |

---

## Setup (Local Development)

### 1. Backend API (FastAPI)

```bash
cd Mcd_Malaysia_Project/Mcd_Api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Make sure data/mcd_outlets.db exists
uvicorn main:app --reload
```

### 2. Frontend (Vue 3 + Vite)

```bash
cd Mcd_Malaysia_Project/Mcd_Visualizer
npm install
# Add your Mapbox token to .env as VITE_MAPBOX_TOKEN=...
npm run dev
```

---

## Cloud Deployment

- **Backend (API):**  
  Deployed to [Render](https://render.com/)  
  API URL: `https://mcd-malaysia-project.onrender.com`

- **Frontend (SPA):**  
  Deployed to [Vercel](https://vercel.com/)  
  Frontend URL: `https://mcd-malaysia-project.vercel.app`

**Environment variables:**

- Set `VITE_API_BASE` in your frontend `.env` to point to your API
- Set `VITE_MAPBOX_TOKEN` for Mapbox

---

## Key Technical Decisions

- **FastAPI:** Rapid async API, easy OpenAPI docs, production ready.
- **Vue 3 + Vite:** Fast, modern SPA, easy state and component logic.
- **Mapbox GL JS:** Interactive, high-quality vector maps.
- **Chatbot/NLP:** Rule-based, simple for demo, but easy to upgrade to LLM/GenAI.
- **SQLite:** Lightweight, no setup needed for demo/dev.

---

## Usage

- **View all outlets** on map with popups (address/features)
- **Search by name** (autocomplete, instant zoom)
- **Chatbot:** Ask about features, e.g. “Which KL outlets have birthday party?”
- **Reset Map:** Recenters and zooms out

---

## Architecture
Frontend (Vue+Vite+Mapbox)
          |
       REST API (FastAPI on Render)
          |
    SQLite DB (or upgrade to PostgreSQL)


- `/outlets` – Get all outlet info for map/search
- `/ask` – NLP-powered Q&A (returns JSON with outlets/feature)

---

## Notes

- **CORS enabled** for frontend-backend separation (dev & demo).
- For production, restrict CORS and secure your database/API keys.
- All assets (icons, favicon, etc.) in `/public/assets/` for easy branding.
- NLP is modular: swap out for LLM API if needed.
- Open-source, MIT license.

---

## Demo Video

[📹 Click here to watch/download the demo video)](./videos/demo.mp4)

---

## Credits

- McDonald’s Malaysia (public info), Mapbox, Vue, FastAPI
- Designed and coded by Lorraine Wong
