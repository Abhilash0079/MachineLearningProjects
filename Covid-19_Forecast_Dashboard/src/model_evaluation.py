import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================================
# LOAD DATA
# =====================================================

print("Loading India dataset...")

df = pd.read_csv("data/processed/india_ml_dataset.csv")

df["date"] = pd.to_datetime(df["date"])

print("Dataset Shape:", df.shape)

# =====================================================
# CREATE LAG FEATURES
# =====================================================

df["lag_1"] = df["new_cases"].shift(1)

df["lag_7"] = df["new_cases"].shift(7)

df["lag_14"] = df["new_cases"].shift(14)

# Remove rows created by lagging
df = df.dropna().copy()

print("Shape After Lag Creation:", df.shape)

# =====================================================
# FEATURES
# =====================================================

features = [
    "lag_1",
    "lag_7",
    "lag_14",
    "cases_7d_avg",
    "cases_14d_avg",
    "vaccination_rate",
    "mortality_rate",
    "month",
    "weekday"
]

target = "new_cases"

X = df[features]

y = df[target]

dates = df["date"]

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test, date_train, date_test = train_test_split(
    X,
    y,
    dates,
    test_size=0.20,
    random_state=42
)

print("\nTrain Shape:", X_train.shape)

print("Test Shape:", X_test.shape)

# =====================================================
# LOAD MODELS
# =====================================================

print("\nLoading Models...")

rf_model = joblib.load("models/random_forest.pkl")

xgb_model = joblib.load("models/xgboost_model.pkl")

print("Models Loaded Successfully")

# =====================================================
# PREDICTIONS
# =====================================================

rf_preds = rf_model.predict(X_test)

xgb_preds = xgb_model.predict(X_test)

# =====================================================
# RANDOM FOREST METRICS
# =====================================================

rf_mae = mean_absolute_error(y_test,rf_preds)

rf_rmse = np.sqrt(
    mean_squared_error(y_test,rf_preds)
)

rf_r2 = r2_score(y_test,rf_preds)

# =====================================================
# XGBOOST METRICS
# =====================================================

xgb_mae = mean_absolute_error(y_test,xgb_preds)

xgb_rmse = np.sqrt(
    mean_squared_error(y_test,xgb_preds)
)

xgb_r2 = r2_score(y_test,xgb_preds)

# =====================================================
# CREATE EVALUATION DIRECTORY
# =====================================================

os.makedirs("data/evaluation",exist_ok=True)

# =====================================================
# SAVE RANDOM FOREST PREDICTIONS
# =====================================================

rf_df = pd.DataFrame({
    "date": date_test.values,
    "actual": y_test.values,
    "predicted": rf_preds
})

rf_df = rf_df.sort_values("date")

rf_df.to_csv("data/evaluation/rf_predictions.csv",index=False)

# =====================================================
# SAVE XGBOOST PREDICTIONS
# =====================================================

xgb_df = pd.DataFrame({
    "date": date_test.values,
    "actual": y_test.values,
    "predicted": xgb_preds
})

xgb_df = xgb_df.sort_values("date")

xgb_df.to_csv("data/evaluation/xgb_predictions.csv",index=False)

# =====================================================
# MODEL COMPARISON
# =====================================================

comparison = pd.DataFrame({
    "Model": ["Random Forest","XGBoost"],
    "MAE": [rf_mae,xgb_mae],
    "RMSE": [rf_rmse,xgb_rmse],
    "R2": [rf_r2,xgb_r2]
})

comparison.to_csv("data/evaluation/model_comparison.csv",index=False)

# =====================================================
# PRINT RESULTS
# =====================================================

print("\nMODEL COMPARISON")

print(comparison)

print("\nFiles Created:")

print("data/evaluation/rf_predictions.csv")

print("data/evaluation/xgb_predictions.csv")

print("data/evaluation/model_comparison.csv")

print("\nEvaluation Completed Successfully")