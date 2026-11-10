# Deutsch Lernen

Learn German with picture cards, grouped by category.

## Stack

- FastAPI + PostgreSQL
- React + Vite + Tailwind + shadcn/ui

## Run

PostgreSQL database: `deutsch_lernen` (user `deutsch`).

```bash
# Backend
cd backend
./venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — login or register, then pick a category (Essen, Tiere, Familie, Farben, Haus, Kleidung).
