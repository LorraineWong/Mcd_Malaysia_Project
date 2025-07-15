# 🍔 McDonald's Outlets in Kuala Lumpur, Malaysia

A modern full-stack web app to **visualize**, **search**, and **chat** about McDonald’s outlets in **Kuala Lumpur, Malaysia**.

- 🔗 [Live Frontend (Vercel)](https://mcd-malaysia-project.vercel.app)  
- 🔗 [Live API Docs (Render)](https://mcd-malaysia-project.onrender.com/docs)

---

## 🚀 Features

- **Interactive Map**: View all McDonald's outlets in KL with 5km catchment zone.
- **LLM-Powered Chatbot**: Ask questions like “Which outlets in KL are open 24 hours?” and get intelligent answers powered by **Gemini (Google Generative AI)**.
- **Autocomplete Search**: Realtime partial-match search by outlet name with map focus.
- **Outlet Popups**: Address, features, contact, Google/Waze navigation links, and nearby outlet overlap hints.
- **Reset View Button**: One click to recenter and zoom out.
- **Responsive UI**: Optimized for desktop usage.

---

## 🧱 Tech Stack

| Layer       | Tech & Tools                                                  |
|-------------|---------------------------------------------------------------|
| **Frontend** | Vue 3, Vite, Mapbox GL JS, Axios                             |
| **Backend**  | FastAPI (Python), Uvicorn                                    |
| **Database** | SQLite (for demo), PostgreSQL (optional upgrade)             |
| **AI/NLP**   | Google Gemini (Generative AI) for parsing user queries       |
| **Deploy**   | Vercel (frontend SPA) + Render (FastAPI backend)             |

---

## 🛠️ Setup (Local Development)

### 1. Backend API (FastAPI)

```bash
cd Mcd_Malaysia_Project/Mcd_Api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Make sure data/mcd_outlets.db exists or run the scraper
uvicorn main:app --reload
```

### 2. Frontend (Vue 3 + Vite)

```bash
cd Mcd_Malaysia_Project/Mcd_Visualizer
npm install
# Create .env and set:
# VITE_MAPBOX_TOKEN=your_mapbox_token
# VITE_API_BASE=http://localhost:8000
npm run dev
```

---

## ☁️ Cloud Deployment

- **Backend API** → [Render](https://render.com/)  
  `https://mcd-malaysia-project.onrender.com`

- **Frontend SPA** → [Vercel](https://vercel.com/)  
  `https://mcd-malaysia-project.vercel.app`

### Required Environment Variables

#### Frontend (`.env`)
```env
VITE_MAPBOX_TOKEN=your_mapbox_token
VITE_API_BASE=https://mcd-malaysia-project.onrender.com
```

#### Backend (`.env`)
```env
ENV=production
ALLOWED_ORIGINS=https://mcd-malaysia-project.vercel.app
GEMINI_API_KEY=your_gemini_key
```

---

## 🧠 Key Technical Decisions

- **FastAPI** – Simple, performant Python API framework with built-in docs.
- **Vue 3 + Vite** – Modern SPA frontend with modular components.
- **Mapbox GL JS** – High-quality interactive maps.
- **Gemini API (Google Generative AI)** – Parses user queries into structured search.
- **SQLite** – Lightweight and easy to use for demos and prototyping.

---

## 📄 Usage

- **View all outlets** on map with popups (address/features)
- **Search by name** (autocomplete, instant zoom)
- **Chatbot:** Ask about features, e.g. “Which KL outlets have birthday party?”
- **Reset Map:** Recenters and zooms out

---

## 🗺️ Architecture
- **Frontend**: Vue 3 + Vite + Mapbox GL
  - Uses Axios to fetch data
  - Supports search and interactive map
- **Chatbot**: Gemini API (LLM)
  - Parses natural language to extract feature + location
- **Backend API**: FastAPI (on Render)
  - `/outlets` – Get all outlets in Kuala Lumpur
  - `/outlets/{id}` – Get details of a single outlet by ID
  - `/ask` – Ask a question (natural language query) 
- **Database**: SQLite (simple local DB, optional upgrade to PostgreSQL)

---

## 🎬 Demo Video

[📹 Click here to watch/download the demo video)](./videos/demo.mp4)

---

## 👩‍💻 Author

Designed and developed by **Lorraine Wong**

> 🧡 Built for learning, demo, and portfolio use.

---

## 📚 License

MIT License © 2025 Lorraine Wong  
