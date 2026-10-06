"""Question B - Level 2: three automated tests (run with: pytest -v)."""
import os

# Use a separate database for tests so real data is not touched
TEST_DB = "test_predictions.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
os.environ["DB_PATH"] = TEST_DB

from fastapi.testclient import TestClient  # noqa: E402
from app import app  # noqa: E402

client = TestClient(app)

VALID = {
    "Pregnancies": 2, "Glucose": 140, "BloodPressure": 72, "SkinThickness": 30,
    "Insulin": 125, "BMI": 33.5, "DiabetesPedigreeFunction": 0.5, "Age": 45,
}


def test_predict_valid_input():
    r = client.post("/predict", json=VALID)
    assert r.status_code == 200
    data = r.json()
    assert 0 <= data["probability"] <= 1
    assert data["risk_level"] in {"Low", "Moderate", "High"}


def test_predict_rejects_bad_input():
    # Age out of range
    r = client.post("/predict", json={**VALID, "Age": 150})
    assert r.status_code == 422
    assert "Age" in str(r.json())  # error message names the bad field
    # Text where a number is expected
    r = client.post("/predict", json={**VALID, "Glucose": "abc"})
    assert r.status_code == 422


def test_stats_counts_requests():
    before = client.get("/stats").json()["total_requests"]
    client.post("/predict", json=VALID)
    after = client.get("/stats").json()
    assert after["total_requests"] == before + 1
    assert 0 <= after["high_risk_share"] <= 1
    assert 0 <= after["average_predicted_risk"] <= 1
