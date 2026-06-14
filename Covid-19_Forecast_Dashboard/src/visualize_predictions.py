import pandas as pd
import matplotlib.pyplot as plt
import os

# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

os.makedirs("reports/figures", exist_ok=True)

# =====================================================
# LOAD FILES
# =====================================================

rf = pd.read_csv("data/evaluation/rf_predictions.csv")
xgb = pd.read_csv("data/evaluation/xgb_predictions.csv")
comparison = pd.read_csv("data/evaluation/model_comparison.csv")

# =====================================================
# RANDOM FOREST
# =====================================================

plt.figure(figsize=(15,6))

plt.plot(
    rf['date'],
    rf['actual'],
    label="Actual"
)

plt.plot(
    rf['date'],
    rf['predicted'],
    label="Predicted"
)

plt.title("Random Forest : Actual vs Predicted")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/random_forest_prediction.png")
plt.close()

# =====================================================
# XGBOOST
# =====================================================

plt.figure(figsize=(15,6))

plt.plot(
    xgb['date'],
    xgb['actual'],
    label="Actual"
)

plt.plot(
    xgb['date'],
    xgb['predicted'],
    label="Predicted"
)

plt.title("XGBOOST : Actual vs Predicted")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/xgboost_prediction.png")
plt.close()

# =====================================================
# MODEL COMPARISON (R2)
# =====================================================

plt.figure(figsize=(8,5))
plt.bar(comparison['Model'], comparison['R2'])
plt.title("Model Comparison - R2")
plt.ylabel("R2 Score")
plt.tight_layout()
plt.savefig("reports/figures/model_r2_comparison.png")
plt.close()

print("\nVisualizations Generated Successfully.")