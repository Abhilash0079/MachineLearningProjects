import pandas as pd
import numpy as np
import joblib
import os

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv('data/processed/india_ml_dataset.csv')

model = joblib.load("models/xgboost_model.pkl")

# ==========================================
# CREATE LAGS
# ==========================================

df['lag_1'] = df['new_cases'].shift(1)
df['lag_7'] = df['new_cases'].shift(7)
df['lag_14'] = df['new_cases'].shift(14)

df = df.dropna().copy()

# ==========================================
# LAST AVAILABLE DATE
# ==========================================

valid_df = df[df["total_cases"] > 0].copy()
last_date = pd.to_datetime(valid_df["date"]).max()
history = (valid_df["new_cases"].tail(14).tolist())

# ==========================================
# CREATE FORECAST INPUT
# ==========================================

future_rows = []
for i in range(1, 31):
    forecast_date = (last_date +pd.Timedelta(days=i))
    
    lag_1 = history[-1]
    lag_7 = history[-7]
    lag_14 = history[-14]
    
    cases_7d_avg = np.mean(history[-7:])
    cases_14d_avg = np.mean(history[-14:])

    input_df = pd.DataFrame({
        "lag_1": [lag_1],
        "lag_7": [lag_7],
        "lag_14": [lag_14],
        "cases_7d_avg": [cases_7d_avg],
        "cases_14d_avg": [cases_14d_avg],
        "vaccination_rate": [valid_df["vaccination_rate"].iloc[-1]],
        "mortality_rate": [valid_df["mortality_rate"].iloc[-1]],
        "month": [forecast_date.month],
        "weekday": [forecast_date.weekday()]
    })

    prediction = model.predict(input_df)[0]
    prediction = max(prediction,0)

    future_rows.append({
        "date": forecast_date,
        "predicted_cases": round(prediction)
    })

    history.append(prediction)
    history = history[-14:]

forecast_df = pd.DataFrame(future_rows)

os.makedirs('data/forecast', exist_ok=True)

forecast_df.to_csv(
    'data/forecast/xgboost_forecast.csv', index=False
)

print(forecast_df.head())
print("\nForecast Saved Successfully.")