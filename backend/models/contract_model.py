# backend/models/contract_model.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from core.db import Base

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    file_path = Column(Text, nullable=False)
    summary = Column(Text)
    analysis_status = Column(String(50), default="Pending")
