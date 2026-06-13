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

last_date = pd.to_datetime(df['date']).max()

# ==========================================
# CREATE FORECAST INPUT
# ==========================================

latest = df.iloc[-1].copy()
future_rows = []

for i in range(1,31):
    forecast_date = (last_date + pd.Timedelta(days=i))
    row = latest.copy()

    row['date'] = forecast_date

    input_df = pd.DataFrame({
        "lag_1": [row["lag_1"]],
        "lag_7": [row["lag_7"]],
        "lag_14": [row["lag_14"]],
        "cases_7d_avg": [row["cases_7d_avg"]],
        "cases_14d_avg": [row["cases_14d_avg"]],
        "vaccination_rate": [row["vaccination_rate"]],
        "mortality_rate": [row["mortality_rate"]],
        "month": [forecast_date.month],
        "weekday": [forecast_date.weekday()]
    })

    prediction = model.predict(input_df)[0]

    future_rows.append({
        'date': forecast_date,
        'predicted_cases': max(prediction,0)
    })

forecast_df = pd.DataFrame(future_rows)

os.makedirs('data/forecast', exist_ok=True)

forecast_df.to_csv(
    'data/forecast/xgboost_forecast.csv', index=False
)

print(forecast_df.head())
print("\nForecast Saved Successfully.")