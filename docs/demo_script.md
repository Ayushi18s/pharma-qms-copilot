# AIVOA Demo Video Script

## Opening
"I built an AI-powered customer complaint management workflow for a pharmaceutical API/FDF quality assurance team. The goal is to take an unstructured customer email or complaint PDF, structure it into a QMS complaint record, and provide a preliminary AI risk assessment for QA review."

## Live demo
"I will start with a customer complaint about discolored Amoxicillin capsules. I paste the raw complaint into the AIVOA Copilot and submit it."

"The backend sends this to a LangGraph workflow. The first node extracts structured complaint fields, the second checks completeness, and the third produces a preliminary risk assessment."

"The extracted data now populates the Log Customer Complaint form. Importantly, the fields remain editable so a QA user can correct the AI output before committing it."

"The Copilot also shows the suggested severity, risk level, risk score, reasoning, root-cause investigation recommendation and CAPA recommendation. These are advisory outputs, not automatic QA decisions."

"I can now commit the complaint to the QMS ledger."

## PDF demo
"The same workflow supports a PDF complaint report. I upload the sample pharmaceutical complaint. FastAPI receives the file and extracts text with pypdf because production OCR is not required for this assignment. The same LangGraph workflow then processes the extracted text."

## Code walkthrough
"On the frontend, Redux holds the structured complaint and risk state. The frontend calls FastAPI. FastAPI invokes the LangGraph graph. Each LangGraph node has one responsibility, which keeps the workflow testable and extensible. The Groq client is isolated in llm.py, and the database layer persists committed complaints."

## Closing
"The prototype is intentionally focused on the complaint-intake and triage workflow. A production implementation would add authentication, audit trails, role-based QA approvals, site SOP integration, validated document handling, and controlled model evaluation."
