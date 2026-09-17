from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.session import Base, engine
from app.api.complaints import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AIVOA AI Complaint Management System", version="1.0.0")
origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.get("/")
def root(): return {"name":"AIVOA Complaint Management API", "status":"ok"}

@app.get("/health")
def health(): return {"status":"healthy", "ai_mock_mode":settings.ai_mock_mode, "model":settings.groq_model}
