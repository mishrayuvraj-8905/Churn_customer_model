import joblib
import pandas as pd

MODEL_PATH = "saved_model/churn_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_churn(customer_dict : dict):
    data = pd.DataFrame([customer_dict])

    probability = model.predict_proba(data)[0][1]

    threshold = 0.45
    prediction = 1 if probability >= threshold else 0

    return prediction, probability