# AIVOA – AI-Powered Customer Complaint Management System

An AI-powered customer complaint management system designed for pharmaceutical quality management. The application converts unstructured customer complaints from text, email, or documents into structured complaint records, performs AI-assisted risk assessment, checks information completeness, and provides root-cause and CAPA recommendations.

## Features

* **AI Complaint Extraction** – Converts unstructured complaint text into structured complaint fields.
* **Multi-format Input** – Supports complaint text, email content, PDF, TXT, and EML files.
* **AI Risk Assessment** – Evaluates complaint severity, risk level, and recommended actions.
* **Completeness Checker** – Identifies missing information required for complaint processing.
* **Root Cause Recommendation** – Generates potential root-cause investigation areas.
* **CAPA Recommendation** – Suggests corrective and preventive actions for quality teams.
* **Duplicate Detection** – Identifies potentially similar complaints using existing complaint records.
* **Editable Complaint Form** – Allows users to review and modify AI-generated information before submission.
* **QMS Complaint Ledger** – Stores and displays logged complaints with their risk and status information.
* **AI Copilot** – Provides an AI-assisted quality assessment before the complaint is committed.
* **LangGraph Workflow** – Orchestrates complaint extraction, completeness checking, and risk assessment.
* **PostgreSQL / SQLite Support** – PostgreSQL-ready persistence with SQLite available for local development.

## Technology Stack

### Frontend

* React
* Redux
* JavaScript
* Inter Font

### Backend

* Python
* FastAPI
* SQLAlchemy
* LangGraph

### AI

* Groq
* `openai/gpt-oss-20b`
* Structured AI outputs for complaint analysis and quality recommendations

### Database

* PostgreSQL
* SQLite for local development

## Application Workflow

```text
Customer Complaint
       |
       v
Text / Email / PDF / TXT / EML
       |
       v
React Frontend
       |
       v
FastAPI Backend
       |
       v
LangGraph Workflow
       |
       +---- Complaint Extraction
       |
       +---- Completeness Check
       |
       +---- AI Risk Assessment
       |
       +---- Root Cause Recommendation
       |
       +---- CAPA Recommendation
       |
       v
Structured Complaint
       |
       +---- Editable Complaint Form
       |
       +---- AI Copilot
       |
       v
QMS Complaint Ledger
```

## AI-Assisted Quality Assessment

The system uses AI to assist quality teams with early complaint triage and investigation support.

The AI generates:

* Risk classification
* Risk score
* Severity assessment
* Reasoning
* Suggested action
* Missing information
* Potential root causes
* CAPA recommendations
* Potential duplicate complaints

AI-generated outputs are intended as **decision-support recommendations** and require review by qualified quality personnel before operational or regulatory action.

## Demo

### Demo Video

[Watch the project demonstration](YOUR_VIDEO_LINK_HERE)

The demonstration covers:

1. Complaint submission through text input
2. AI-powered complaint extraction
3. Structured complaint form population
4. Completeness assessment
5. AI risk assessment
6. Root-cause and CAPA recommendations
7. Editing complaint information
8. Committing the complaint to the QMS ledger
9. Duplicate complaint detection
10. PDF complaint analysis

### Sample Data

Example complaint documents are available in the [`sample_data`](./sample_data) directory.

## Project Structure

```text
aivoa_assignment/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── index.html
│
├── sample_data/
│   ├── sample_customer_email.txt
│   ├── sample_discoloration_complaint.pdf
│   └── sample_foreign_matter_complaint.pdf
│
├── docs/
├── docker-compose.yml
├── start_backend.sh
├── start_frontend.sh
└── README.md
```

## Local Setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Groq API key to `.env`:

```env
GROQ_API_KEY=your_key_here
AI_MOCK_MODE=false
```

For local development, SQLite can be used:

```env
DATABASE_URL=sqlite:///./aivoa.db
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

API:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The application will normally be available at:

```text
http://localhost:5173
```

## PostgreSQL

The project also supports PostgreSQL through Docker Compose.

```bash
docker compose up --build
```

Configure the backend with:

```env
DATABASE_URL=postgresql+psycopg://aivoa:aivoa_dev_password@localhost:5432/aivoa
```

## Project Purpose

This system demonstrates how generative AI, workflow orchestration, and modern web technologies can be combined to streamline pharmaceutical customer complaint intake and early quality assessment while keeping human review in the decision-making process.

## Author

**Ayushi**

B.Tech – Computer Science & Engineering (Data Science)

[GitHub](https://github.com/Ayushi18s)
