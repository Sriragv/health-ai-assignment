"""Question A - Level 1: Clean Pima diabetes data, train LR + RF."""
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

S = 59  # USN ends in I059 -> numeric part 0059 = 59

df = pd.read_csv("diabetes.csv")

# Cleaning: 0 is impossible for these columns -> treat as missing, fill with median
zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
for col in zero_as_missing:
    print(f"{col}: {(df[col] == 0).sum()} zeros replaced")
    df[col] = df[col].replace(0, np.nan)
    df[col] = df[col].fillna(df[col].median())

X = df.drop(columns="Outcome")
y = df["Outcome"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=S, stratify=y
)

models = {
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(random_state=S, max_iter=1000)),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=S),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"\n{name}")
    print(f"  Accuracy : {accuracy_score(y_test, pred):.3f}")
    print(f"  Precision: {precision_score(y_test, pred):.3f}")
    print(f"  Recall   : {recall_score(y_test, pred):.3f}")

# Save LR pipeline for Question B
joblib.dump(models["Logistic Regression"], "model.joblib")
X_train.join(y_train).to_csv("train.csv", index=False)
X_test.join(y_test).to_csv("test.csv", index=False)
print("\nSaved model.joblib, train.csv, test.csv")
