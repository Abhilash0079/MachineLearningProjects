import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

#========================================
# LOAD DATA
#========================================

df = pd.read_csv("data/processed/india_ml_dataset.csv")
df['date'] = pd.to_datetime(df['date'])

#========================================
# LAG FEATURES
#========================================

df['lag_1'] = df['new_cases'].shift(1)
df['lag_7'] = df['new_cases'].shift(7)
df['lag_14'] = df['new_cases'].shift(14)

# =====================================================
# REMOVE NULLS
# =====================================================

df = df.dropna()

# =====================================================
# FEATURES
# =====================================================

features = [
    'lag_1','lag_7','lag_14',
    'cases_7d_avg', 'cases_14d_avg',
    'vaccination_rate', 'mortality_rate',
    'month', 'weekday'
]

X = df[features]
y = df['new_cases']

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================================
# MODEL
# =====================================================

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# =====================================================
# PREDICT
# =====================================================

preds = model.predict(X_test)

# =====================================================
# METRICS
# =====================================================

mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)

print("\nXGBOOST RESULTS: ")
print(f"MAE : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R2 : {r2:,.4f}")

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values("Importance", ascending=False)

print("\nFeature Importance")
print(importance)

# =====================================================
# SAVE MODEL
# =====================================================

os.makedirs("models", exist_ok=True)

joblib.dump(model,"models/xgboost_model.pkl")
print("\nModel Saved Successfully.")
