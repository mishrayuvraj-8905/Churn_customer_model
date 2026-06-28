import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

st.title("Customer Churn Prediction Dashboard")

tab1, tab2, tab3 = st.tabs(["Predict Churn", "Predictions", "Analytics"])

with tab1:
    st.subheader("Enter Customer Details")

    gender = st.selectbox("Gender", ["Male", "Female"])
    senior_citizen = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.number_input("Tenure", min_value=0, max_value=100, value=12)

    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
        ],
    )

    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=80.0)
    total_charges = st.number_input("Total Charges", min_value=0.0, value=800.0)

    if st.button("Predict"):
        payload = {
            "gender": gender,
            "senior_citizen": senior_citizen,
            "partner": partner,
            "dependents": dependents,
            "tenure": tenure,
            "phone_service": phone_service,
            "multiple_lines": multiple_lines,
            "internet_service": internet_service,
            "online_security": online_security,
            "online_backup": online_backup,
            "device_protection": device_protection,
            "tech_support": tech_support,
            "streaming_tv": streaming_tv,
            "streaming_movies": streaming_movies,
            "contract": contract,
            "paperless_billing": paperless_billing,
            "payment_method": payment_method,
            "monthly_charges": monthly_charges,
            "total_charges": total_charges,
        }

        response = requests.post(f"{API_URL}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success("Prediction successful")
            st.metric("Churn Prediction", result["churn_prediction"])
            st.metric("Churn Probability", round(result["churn_probability"], 4))
            st.metric("Risk Level", result["risk_level"])
        else:
            st.error(response.text)

with tab2:
    st.subheader("Saved Predictions")

    if st.button("Load Predictions"):
        response = requests.get(f"{API_URL}/predictions?skip=0&limit=100")

        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found.")
        else:
            st.error(response.text)

    delete_id = st.number_input("Delete Prediction ID", min_value=1, step=1)

    if st.button("Delete Prediction"):
        response = requests.delete(f"{API_URL}/predictions/{delete_id}")

        if response.status_code == 200:
            st.success("Deleted successfully")
        else:
            st.error(response.text)

with tab3:
    st.subheader("Analytics Summary")

    if st.button("Load Analytics"):
        response = requests.get(f"{API_URL}/analytics/summary")

        if response.status_code == 200:
            data = response.json()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Predictions", data["total_predictions"])
            col2.metric("High Risk", data["high_risk"])
            col3.metric("Medium Risk", data["medium_risk"])
            col4.metric("Low Risk", data["low_risk"])

            st.metric(
                "Average Churn Probability",
                data["average_churn_probability"],
            )
        else:
            st.error(response.text)