"""Question A - Level 2: Logistic regression + confusion matrix from scratch (NumPy only).
scikit-learn is used ONLY to load the Level 1 model for comparison."""
import numpy as np
import pandas as pd
import joblib

S = 59  # USN ends in I059 -> numeric part 0059 = 59

# Same split as Level 1 (saved by train_level1.py)
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")
features = [c for c in train.columns if c != "Outcome"]
X_train, y_train = train[features].values, train["Outcome"].values
X_test, y_test = test[features].values, test["Outcome"].values

# Standardize using TRAIN statistics only (same as sklearn's StandardScaler)
mu, sd = X_train.mean(axis=0), X_train.std(axis=0)
X_train_s = (X_train - mu) / sd
X_test_s = (X_test - mu) / sd


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def log_loss(y, p):
    p = np.clip(p, 1e-12, 1 - 1e-12)  # avoid log(0)
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


def train_logreg(X, y, lr=0.1, epochs=5000, seed=S):
    rng = np.random.default_rng(seed)
    w = rng.normal(0, 0.01, X.shape[1])
    b = 0.0
    n = len(y)
    for epoch in range(epochs):
        p = sigmoid(X @ w + b)          # predictions
        dw = X.T @ (p - y) / n          # gradient of loss w.r.t. weights
        db = np.mean(p - y)             # gradient w.r.t. bias
        w -= lr * dw                    # gradient descent step
        b -= lr * db
        if epoch % 1000 == 0:
            print(f"  epoch {epoch:4d}  loss {log_loss(y, p):.4f}")
    print(f"  final      loss {log_loss(y, sigmoid(X @ w + b)):.4f}")
    return w, b


def confusion_matrix(y_true, y_pred):
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    return tp, tn, fp, fn


def report(name, y_true, y_pred):
    tp, tn, fp, fn = confusion_matrix(y_true, y_pred)
    acc = (tp + tn) / len(y_true)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    print(f"\n{name}")
    print(f"  Confusion matrix:  TP={tp}  FP={fp}  FN={fn}  TN={tn}")
    print(f"  Accuracy {acc:.3f} | Precision {prec:.3f} | Recall {rec:.3f}")
    return acc


print("Training NumPy logistic regression...")
w, b = train_logreg(X_train_s, y_train)
my_probs = sigmoid(X_test_s @ w + b)
my_pred = (my_probs >= 0.5).astype(int)
my_acc = report("My NumPy model", y_test, my_pred)

# Comparison with the sklearn model from Level 1
sk_model = joblib.load("model.joblib")
sk_pred = sk_model.predict(test[features])
sk_acc = report("scikit-learn model", y_test, sk_pred)
print(f"\nAccuracy difference: {abs(my_acc - sk_acc):.3f}")

# Top 3 features by absolute weight (both models use standardized inputs)
sk_w = sk_model[-1].coef_[0]
top3 = np.argsort(-np.abs(w))[:3]
print("\nTop 3 features (my model)   my_weight   sklearn_weight")
for i in top3:
    print(f"  {features[i]:<26}{w[i]:>9.3f}   {sk_w[i]:>12.3f}")

# Save probabilities for Level 3
np.save("my_test_probs.npy", my_probs)
