#=====================================
# STEP 5 — Lag Feature Engineering & Model Training
#=====================================

import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

#=====================================
# LOAD DATA
#=====================================

df = pd.read_csv('data/processed/india_ml_dataset.csv')

df['date'] = pd.to_datetime(df['date'])
print(f"Original Shape: {df.shape}")

#=====================================
# CREATE LAG FEATURES
#=====================================

df['lag_1'] = df['new_cases'].shift(1)
df['lag_7'] = df['new_cases'].shift(7)
df['lag_14'] = df['new_cases'].shift(14)

#=====================================
# REMOVE MULES CREATED BY LAGS
#=====================================

df.dropna()
print(f"Shape After Lag Creation: {df.shape}")

#=====================================
# FEATURES
#=====================================

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

target = 'new_cases'

X = df[features]
y = df[target]

#=====================================
# TRAIN TEST SPLIT
#=====================================

X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.2,
    random_state=42
)

print("\nTrain Shape:", X_train.shape)
print("\nTest Shape:", X_test.shape)

#=====================================
# MODEL
#=====================================

rf = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

#=====================================
# PREDDICTIONS
#=====================================

preds = rf.predict(X_test)

#=====================================
# EVALUATION
#=====================================

mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)

print("\nMODEL PERFORMANCE")
print(f"MAE : {mae:,.2f}")
print(f"RMSE : {rmse:,.2f}")
print(f"R2 : {r2:,.4f}")

#=====================================
# FEATURE IMPORTANCE
#=====================================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": rf.feature_importances_
})

importance = importance.sort_values(
    "Importance", ascending=False
)

print("\nFeature Importance")
print(importance)

#=====================================
# SAVE MODEL
#=====================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    rf,
    "models/random_forest.pkl"
)

print("\nModel Saved Successfully.")