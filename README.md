# AIVOA – AI-Powered Customer Complaint Management System

Round 1 implementation for the AIVOA AI Product Engineer (Interns) assignment.

## What is implemented

- React + Redux frontend
- Python + FastAPI backend
- LangGraph complaint-processing workflow
- Groq LLM integration with assignment-requested `gemma2-9b-it` plus configurable fallback
- PostgreSQL-ready persistence (SQLite works without Docker)
- Inter font
- Complaint text/email input
- PDF/TXT/EML upload
- AI complaint extraction and structured form population
- AI Copilot preliminary risk assessment
- Complaint completeness checker
- Root-cause recommendation
- CAPA recommendation
- Possible duplicate detection using existing product/batch records
- QMS complaint ledger
- Editable fields before commit

## Important model compatibility note

The assignment specifies Groq `gemma2-9b-it`. Groq's current documentation marks that model as deprecated with a shutdown date of October 8, 2025, and recommends `llama-3.1-8b-instant`. The code therefore keeps `GROQ_MODEL=gemma2-9b-it` to reflect the assignment while automatically trying `GROQ_FALLBACK_MODEL` if the requested model is unavailable. See the current Groq documentation before the final demo.

## Local setup on macOS

### 1. Prerequisites

Install Node.js 20+ and Python 3.11+.

Optional: Docker Desktop if you want PostgreSQL.

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Put your Groq API key in `.env`:

```env
GROQ_API_KEY=your_key_here
AI_MOCK_MODE=false
```

For the simplest local demo, keep `DATABASE_URL=sqlite:///./aivoa.db`.

Run:

```bash
uvicorn app.main:app --reload --port 8000
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

### 3. Frontend

Open another Terminal tab:

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally http://localhost:5173.

### 4. PostgreSQL option

From the repository root:

```bash
docker compose up --build
```

Then set the backend environment to:

```env
DATABASE_URL=postgresql+psycopg://aivoa:aivoa_dev_password@localhost:5432/aivoa
```

If running the backend directly on macOS while Postgres is in Docker, use `localhost`. If the backend itself is inside Compose, the service name `db` is used by the provided Compose environment.

## Demo flow

1. Open the application.
2. Click **Load demo complaint**.
3. Send the complaint.
4. Watch the LangGraph workflow extract structured fields.
5. Show the populated complaint form.
6. Show completeness and AI risk assessment.
7. Edit a field if desired.
8. Click **Commit to QMS Ledger**.
9. Open **Complaint Ledger** to show persistence.
10. Upload one of the sample PDFs in `sample_data/` and demonstrate document analysis.

## Architecture

```text
React UI
  |
  | Redux state
  v
FastAPI
  |
  v
LangGraph
  |-- Extract Complaint
  |-- Check Completeness
  |-- Risk Assessment
  v
Groq LLM
  |
  v
Structured JSON
  |
  +--> React complaint form
  +--> AI Copilot risk panel
  +--> PostgreSQL / SQLite QMS ledger
```

## QMS framing

This prototype is an AI-assisted intake and triage tool, not a replacement for QA approval or site SOPs. AI risk and CAPA outputs are recommendations that require human QA review.

## Suggested 5–10 minute video structure

- 0:00–0:45: Problem and QMS use case
- 0:45–2:00: Complaint text intake
- 2:00–3:00: LangGraph extraction and form population
- 3:00–4:00: Risk assessment + completeness
- 4:00–5:00: Edit and commit to ledger
- 5:00–6:00: PDF upload
- 6:00–7:30: Code walkthrough: React → FastAPI → LangGraph → Groq → DB
- 7:30–8:30: Bonus features
- 8:30–9:00: Architecture and limitations
