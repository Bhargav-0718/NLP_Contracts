# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import contracts, reports

app = FastAPI(title="Contract Summarization & Clause Review API")

# CORS setup for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/")
def root():
    return {"message": "Contract Summarization & Clause Review API running 🚀"}
