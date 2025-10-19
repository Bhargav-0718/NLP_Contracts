# backend/models/report_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from datetime import datetime
from core.db import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    report_path = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    tier_distribution = Column(JSON)
    summary_score = Column(Float)
