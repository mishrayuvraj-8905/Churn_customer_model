from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from app.database import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)

    gender = Column(String)
    senior_citizen = Column(Integer)
    partner = Column(String)
    dependents = Column(String)
    tenure = Column(Integer)

    phone_service = Column(String)
    multiple_lines = Column(String)
    internet_service = Column(String)
    online_security = Column(String)
    online_backup = Column(String)
    device_protection = Column(String)
    tech_support = Column(String)
    streaming_tv = Column(String)
    streaming_movies = Column(String)

    contract = Column(String)
    paperless_billing = Column(String)
    payment_method = Column(String)

    monthly_charges = Column(Float)
    total_charges = Column(Float)

    churn_prediction = Column(Integer)
    churn_probability = Column(Float)
    risk_level = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)