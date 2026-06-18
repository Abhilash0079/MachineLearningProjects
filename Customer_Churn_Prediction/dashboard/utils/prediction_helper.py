import pandas as pd
import numpy as np
import joblib

#=============================
# LOAD ARTIFACTS
#=============================
model = joblib.load("models/logistic_regression_churn.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

HIGH_VALUE_THRESHOLD = 70.35

#=========================
# PREDICT CHURN
#=========================
def predict_customer(data):
    df =pd.DataFrame([data])

    #=====================
    # feature engineering
    #=====================
    df["AvgMonthlySpend"] = np.where(
        df['tenure']>0,
        df['TotalCharges']/df['tenure'],0
    )

    df['IsLongTermCustomer'] = np.where(
        df['tenure']>=24, 1,0
    )

    df['IsHighValueCustomer'] = np.where(
        df['MonthlyCharges']>HIGH_VALUE_THRESHOLD,1,0
    )

    df['HasFamily'] = np.where(
        (df['Partner'] == 1) | (df['Dependents']==1),1,0
    )

    services = [
        "PhoneService",
        "MultipleLines",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]
    count = 0
    for col in services:
        if col=="PhoneServices":
            count+=int(df[col].iloc[0])
        else:
            count+=int(df[col].iloc[0]=="Yes")
    
    df["NumServices"]=count

    #========================
    # tenure group
    #========================
    tenure = df['tenure'].iloc[0]
    if tenure<=12:
        group="New"
    elif tenure<=24:
        group="Developing"
    elif tenure<=48:
        group="Established"
    else:
        group="Loyal"
    
    df["TenureGroup"] = group

    #=====================
    # dummies
    #=====================
    dummy_cols = [
        "gender",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaymentMethod",
        "TenureGroup"
    ]
    df = pd.get_dummies(df, columns=dummy_cols, drop_first=True)

    #===========================
    # missing columns
    #===========================
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_columns]

    #=========================
    # scaling
    #========================
    scaled= scaler.transform(df)

    #========================
    # prediction
    #=======================
    probability = model.predict_proba(scaled)[0][1]
    prediction = int(probability>=0.5)

    return prediction, probability