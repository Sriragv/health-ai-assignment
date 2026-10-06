"""Question A - Level 3: Lower the decision threshold until recall >= 0.9.
Uses probabilities from my NumPy model (saved by level2_scratch.py)."""
import numpy as np
import pandas as pd

S = 59  # USN ends in I059 -> numeric part 0059 = 59

test = pd.read_csv("test.csv")
y = test["Outcome"].values
probs = np.load("my_test_probs.npy")


def confusion_matrix(y_true, y_pred):
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    return tp, tn, fp, fn


def metrics(threshold):
    tp, tn, fp, fn = confusion_matrix(y, (probs >= threshold).astype(int))
    acc = (tp + tn) / len(y)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return acc, prec, rec, tp, fp, fn, tn


print(f"Test set: {len(y)} patients, {y.sum()} diabetic\n")
print("Threshold  Accuracy  Precision  Recall   TP  FP  FN   TN")
for t in np.arange(0.90, 0.04, -0.05):
    acc, prec, rec, tp, fp, fn, tn = metrics(t)
    print(f"  {t:.2f}      {acc:.3f}     {prec:.3f}     {rec:.3f}   {tp:3d} {fp:3d} {fn:3d}  {tn:3d}")

# Highest threshold that still gives recall >= 0.9 (fine-grained search)
for t in np.arange(0.50, 0.0, -0.01):
    acc, prec, rec, tp, fp, fn, tn = metrics(t)
    if rec >= 0.9:
        print(f"\nRecall >= 0.9 first reached at threshold {t:.2f}:")
        print(f"  Accuracy {acc:.3f} | Precision {prec:.3f} | Recall {rec:.3f}")
        print(f"  TP={tp} FP={fp} FN={fn} TN={tn}")
        break

# Why accuracy misleads: a 'model' that says nobody is diabetic
dumb_acc = np.mean(y == 0)
print(f"\nBaseline 'predict nobody is diabetic': accuracy {dumb_acc:.3f}, recall 0.000")
