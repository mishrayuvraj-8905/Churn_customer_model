from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.schemas import CustomerData, PredictionResponse
from app.ml_model import predict_churn
from app.database import Base, engine, get_db
from app import db_models
from fastapi import HTTPException

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Welcome to the Customer Churn Prediction API!"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerData, db: Session = Depends(get_db)):
    customer_dict = customer.model_dump()

    model_input = {
        "gender": customer_dict["gender"],
        "SeniorCitizen": customer_dict["senior_citizen"],
        "Partner": customer_dict["partner"],
        "Dependents": customer_dict["dependents"],
        "tenure": customer_dict["tenure"],
        "PhoneService": customer_dict["phone_service"],
        "MultipleLines": customer_dict["multiple_lines"],
        "InternetService": customer_dict["internet_service"],
        "OnlineSecurity": customer_dict["online_security"],
        "OnlineBackup": customer_dict["online_backup"],
        "DeviceProtection": customer_dict["device_protection"],
        "TechSupport": customer_dict["tech_support"],
        "StreamingTV": customer_dict["streaming_tv"],
        "StreamingMovies": customer_dict["streaming_movies"],
        "Contract": customer_dict["contract"],
        "PaperlessBilling": customer_dict["paperless_billing"],
        "PaymentMethod": customer_dict["payment_method"],
        "MonthlyCharges": customer_dict["monthly_charges"],
        "TotalCharges": customer_dict["total_charges"],
    }

    prediction, probability = predict_churn(model_input)

    prediction = int(prediction)
    probability = float(probability)

    if probability >= 0.70:
        risk_level = "High Risk"
    elif probability >= 0.45:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    new_prediction = db_models.PredictionLog(
        **customer_dict,
        churn_prediction=prediction,
        churn_probability=probability,
        risk_level=risk_level,
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {
        "id": new_prediction.id,
        "churn_prediction": prediction,
        "churn_probability": probability,
        "risk_level": risk_level,
    }


@app.get("/predictions", response_model=list[PredictionResponse])
def get_predictions(
    skip: int = 0,
    limit: int = 10,
    risk_level: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(db_models.PredictionLog)

    if risk_level:
        query = query.filter(db_models.PredictionLog.risk_level == risk_level)

    return query.offset(skip).limit(limit).all()


@app.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    total_predictions = db.query(db_models.PredictionLog).count()

    high_risk = db.query(db_models.PredictionLog).filter(
        db_models.PredictionLog.risk_level == "High Risk"
    ).count()

    medium_risk = db.query(db_models.PredictionLog).filter(
        db_models.PredictionLog.risk_level == "Medium Risk"
    ).count()

    low_risk = db.query(db_models.PredictionLog).filter(
        db_models.PredictionLog.risk_level == "Low Risk"
    ).count()

    avg_probability = db.query(
        func.avg(db_models.PredictionLog.churn_probability)
    ).scalar()

    return {
        "total_predictions": total_predictions,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "average_churn_probability": round(avg_probability or 0, 4),
    }


@app.delete("/predictions/{prediction_id}")
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(db_models.PredictionLog).filter(
        db_models.PredictionLog.id == prediction_id
    ).first()

    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    db.delete(prediction)
    db.commit()

    return {"message": "Prediction deleted successfully"}

@app.delete("/predictions")
def delete_all_predictions(db: Session = Depends(get_db)):
    deleted = db.query(db_models.PredictionLog).delete()
    db.commit()

    return {
        "message": "All predictions deleted successfully",
        "deleted_records": deleted
    }