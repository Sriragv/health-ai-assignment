"""Question B - Levels 1 & 2: FastAPI app serving the Question A diabetes model.
Level 1: /predict endpoint + HTML page showing risk in plain words.
Level 2: every request saved in SQLite, /stats with hand-written SQL (no ORM),
         input validation with clear error messages."""
import os
import sqlite3
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

BASE = Path(__file__).parent
MODEL_PATH = BASE.parent / "question_A" / "model.joblib"
DB_PATH = os.environ.get("DB_PATH", str(BASE / "predictions.db"))
THRESHOLD = 0.25  # chosen in Question A Level 3 (recall 0.926)

FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    print(f"WARNING: model file not found at {MODEL_PATH}. /predict will return 503.")

app = FastAPI(title="Diabetes Risk API")


# ---------- Input validation (Level 2) ----------
class PatientInput(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=20)
    Glucose: float = Field(..., ge=1, le=300)          # mg/dL
    BloodPressure: float = Field(..., ge=1, le=200)    # mm Hg
    SkinThickness: float = Field(..., ge=1, le=100)    # mm
    Insulin: float = Field(..., ge=1, le=900)          # mu U/ml
    BMI: float = Field(..., ge=10, le=80)
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3)
    Age: int = Field(..., ge=1, le=120)


# ---------- Database (Level 2, raw SQL, no ORM) ----------
def run_sql(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.fetchone() if fetch else None
    finally:
        conn.close()


def init_db():
    run_sql("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            pregnancies INTEGER, glucose REAL, blood_pressure REAL,
            skin_thickness REAL, insulin REAL, bmi REAL, dpf REAL, age INTEGER,
            probability REAL NOT NULL,
            is_high_risk INTEGER NOT NULL
        )
    """)


init_db()


def risk_text(p):
    if p >= 0.5:
        return "High", f"High risk ({p:.0%}). Please talk to a doctor about a blood sugar test."
    if p >= THRESHOLD:
        return "Moderate", f"Moderate risk ({p:.0%}). A check-up with a doctor is a good idea."
    return "Low", f"Low risk ({p:.0%}). Keep up healthy habits and regular check-ups."


# ---------- Endpoints ----------
@app.get("/")
def home():
    return FileResponse(BASE / "index.html")


@app.post("/predict")
def predict(patient: PatientInput):
    if model is None:
        raise HTTPException(status_code=503, detail="The risk model is not available right now. Please try again later.")
    row = pd.DataFrame([patient.model_dump()])[FEATURES]
    prob = float(model.predict_proba(row)[0, 1])
    level, message = risk_text(prob)
    is_high = int(prob >= THRESHOLD)

    run_sql(
        """INSERT INTO predictions
           (created_at, pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, dpf, age, probability, is_high_risk)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (datetime.now().isoformat(timespec="seconds"),
         patient.Pregnancies, patient.Glucose, patient.BloodPressure,
         patient.SkinThickness, patient.Insulin, patient.BMI,
         patient.DiabetesPedigreeFunction, patient.Age, prob, is_high),
    )
    return {
        "probability": round(prob, 3),
        "risk_level": level,
        "message": message,
        "flagged": bool(is_high),
        "note": "Screening estimate only, not a diagnosis.",
    }


@app.get("/stats")
def stats():
    total, avg_prob, high_share = run_sql(
        "SELECT COUNT(*), AVG(probability), AVG(is_high_risk) FROM predictions",
        fetch=True,
    )
    return {
        "total_requests": total,
        "average_predicted_risk": round(avg_prob or 0, 3),
        "high_risk_share": round(high_share or 0, 3),  # share flagged at >= 0.25
    }
