from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.schemas import CustomerData
from app.ml_model import predict_churn
from app.database import Base, engine, get_db
from app import db_models

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Welcome to the Customer Churn Prediction API!"}


@app.post("/predict")
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
        "prediction_id": new_prediction.id,
        "churn_prediction": prediction,
        "churn_probability": probability,
        "risk_level": risk_level,
    }