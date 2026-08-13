import joblib
import pandas as pd

# Load preprocessing pipeline
preprocessing_pipeline = joblib.load("models/preprocessing_pipeline.pkl")

# Load tuned model
model = joblib.load("models/best_model_tuned.pkl")

def predict_price(input_data):
    input_df = pd.DataFrame([input_data])
    input_scaled = preprocessing_pipeline.transform(input_df)
    prediction = model.predict(input_scaled)
    return prediction[0]