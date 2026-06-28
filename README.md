# Customer Churn Prediction Platform

An end-to-end Machine Learning application that predicts customer churn using a trained classification model and serves predictions through a FastAPI backend. The application stores prediction history in PostgreSQL, provides analytics endpoints, and includes a Streamlit dashboard for an interactive user experience.

---

## Features

- Predict customer churn using a trained Machine Learning model
- Calculate churn probability
- Classify customers into High, Medium, and Low Risk
- Store every prediction in PostgreSQL
- Retrieve historical predictions
- Filter predictions by risk level
- View analytics summary of all predictions
- Delete predictions by ID
- Interactive Streamlit dashboard
- Dockerized application for consistent deployment

---

## Tech Stack

### Machine Learning
- Python
- Pandas
- Scikit-learn
- Joblib

### Backend
- FastAPI
- Pydantic
- SQLAlchemy

### Database
- PostgreSQL

### Frontend
- Streamlit

### DevOps
- Docker
- Docker Compose
- Git & GitHub

---

## Project Architecture

```
                     Streamlit Dashboard
                             │
                             ▼
                     FastAPI Backend
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
 Machine Learning Model                 PostgreSQL Database
 (Scikit-learn + Joblib)          (Prediction Logs & Analytics)
```

---

## Project Structure

```
Churn_customer_model/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── db_models.py
│   ├── ml_model.py
│   └── schemas.py
│
├── frontend/
│   └── streamlit_app.py
│
├── saved_model/
│   └── churn_model.pkl
│
├── data/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome endpoint |
| POST | `/predict` | Predict customer churn |
| GET | `/predictions` | Retrieve prediction history |
| GET | `/analytics/summary` | View analytics summary |
| DELETE | `/predictions/{id}` | Delete prediction by ID |

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Churn_customer_model.git

cd Churn_customer_model
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
DATABASE_URL=your_postgresql_database_url
```

Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

Access Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

## Running with Docker

```bash
docker compose up --build
```

---

## Running the Streamlit Dashboard

```bash
streamlit run frontend/streamlit_app.py
```

---

## Example Prediction Response

```json
{
    "id": 15,
    "churn_prediction": 1,
    "churn_probability": 0.8914,
    "risk_level": "High Risk"
}
```

---

## Author

**Yuvraj Mishra**

B.Tech, IIT Bombay
