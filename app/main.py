from fastapi import FastAPI

from app.schemas import CustomerData
from app.ml_model import predict_churn

app=FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Customer Churn Prediction API!"}

@app.post("/predict")
def predict(customer: CustomerData):
    customer_dict = customer.model_dump()

    prediction, probability = predict_churn(customer_dict)

    if probability >=0.70:
        risk_level = "High Risk"

    elif probability >=0.45:
        risk_level = "Medium Risk"

    else:
        risk_level = "Low Risk"

    return {
        "churn_prediction": prediction,
        "churn_probability": probability,
        "risk_level": risk_level
    }