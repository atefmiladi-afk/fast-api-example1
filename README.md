# Deutsch Lernen

Learn German with picture cards, grouped by category.

## Stack

- FastAPI + PostgreSQL
- React + Vite + Tailwind + shadcn/ui

## Run

Copy `backend/.env.example` to `backend/.env` and set `DATABASE_URL`, `SECRET_KEY`, and SMTP settings for verification and password-reset emails.

```bash
# Backend
cd backend
cp .env.example .env
./venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — register, verify the email link, then sign in. Use Forgot password to reset via email.
