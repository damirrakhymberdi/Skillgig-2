# SkillGig 

Monorepo:
- **Frontend**: Vue 3 + Vite (port **5174**)
- **Backend**: FastAPI (port **8000**, API prefix **/api/v1**)

## Local development

### Frontend

1) Create env file (Cursor may block `.env*` edits, so we keep examples as `env.example`)

```bash
copy env.example .env
```

2) Install and run

```bash
npm install
npm run dev
```

### Backend (Docker)

```bash
docker compose up --build
```

Backend will be available at `http://localhost:8000`.

## Environment variables

### Frontend

- `VITE_API_URL`: backend API base URL (must include `/api/v1`)
  - example: `http://localhost:8000/api/v1`

### Backend

Copy `backend/env.example` to `backend/.env` (not committed) and adjust:

- `APP_ENVIRONMENT`: `development` or `production`
- `APP_SECRET_KEY`: change in production
- `APP_DATABASE_URL`: SQLite by default (can be Postgres in production)
- `APP_CORS_ORIGINS`: comma-separated SPA origins (used when `APP_ENVIRONMENT=production`)

## CI (GitHub Actions)

Workflow: `.github/workflows/ci.yml`
- Builds frontend
- Installs backend development deps, runs import/compile checks, and executes API/migration tests

## Deploy (recommended)

- **Backend**: Render / Railway / Fly.io (Docker deploy using `backend/Dockerfile`)
  - set env: `APP_ENVIRONMENT=production`, `APP_SECRET_KEY`, `APP_DATABASE_URL`, `APP_CORS_ORIGINS=https://<your-frontend-domain>`
- **Frontend**: any static hosting (Vercel/Netlify/Cloudflare Pages)
  - set env: `VITE_API_URL=https://<your-backend-domain>/api/v1`

