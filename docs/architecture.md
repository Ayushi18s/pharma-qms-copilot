# Architecture Walkthrough

## Frontend

`src/App.jsx` renders the QMS complaint form and AIVOA Copilot. `src/store/store.js` uses Redux Toolkit to keep complaint, risk, completeness, duplicate and workflow status in one state object.

## API

`POST /api/complaints/analyze` accepts complaint text.

`POST /api/complaints/analyze-file` accepts PDF/TXT/EML uploads as multipart form data.

`POST /api/complaints` commits an approved/editable record to the ledger.

`GET /api/complaints` returns logged complaints.

## AI

`app/ai/graph.py` creates a LangGraph StateGraph:

1. `extract_complaint`
2. `check_completeness`
3. `risk_assessment`

`app/ai/llm.py` isolates Groq calls and supports a configurable fallback model because the assignment's requested Gemma model has since been deprecated by Groq.

## Database

The same SQLAlchemy model works with SQLite for quick local demonstration and PostgreSQL for the final stack demonstration.
