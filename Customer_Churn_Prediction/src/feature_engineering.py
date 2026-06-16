"""
STEP 4: FEATURE ENGINEERING 

Business Logic

We'll create the following features:

Feature	                                    Purpose
AvgMonthlySpend	                        Customer spending behavior
IsSeniorCitizen	                        Explicit binary feature
IsLongTermCustomer	                    Loyalty indicator
IsHighValueCustomer	                    Revenue importance
HasFamily	                            Family dependency indicator
NumServices	                            Service usage intensity
TenureGroup	                            Customer lifecycle stage

"""

import pandas as pd
import numpy as np
import os

#=============================
# LOAD DATA
#=============================
INPUT_FILE = "data/processed/churn_processed.csv"
OUTPUT_FILE = "data/processed/churn_featured.csv"

df = pd.read_csv(INPUT_FILE)
print(f"Shape Before: {df.shape}")

#=============================
# AVG MONTHLY SPEND
#=============================
df['AvgMonthlySpend'] = np.where(
    df['tenure']>0,
    df['TotalCharges']/df['tenure'],
    0
)

#=============================
# LONG TERM CUSTOMER
#=============================
df['IsLongTermCustomer'] = np.where(
    df['tenure']>=24,
    1,
    0
)

#=============================
# HIGH VALUE CUSTOMER
#=============================
median_charge = df['MonthlyCharges'].median()

df['IsHighValueCustomer'] = np.where(
    df['MonthlyCharges']>median_charge,
    1,
    0
)

#=============================
# FAMILY CUSTOMER
#=============================
df['HasFamily'] = np.where(
    (
        (df['Partner'] == "Yes")
        |
        (df['Dependents'] == "Yes")
    ),
    1,
    0
)

#=============================
# NUMBER OF SERVICES
#=============================
service_cols = [
    "PhoneService",
    "MultipleLines",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]

df['NumServices'] = 0

for col in service_cols:
    df['NumServices'] +=np.where(
        df[col].isin(["Yes"]),
        1,
        0
    )

#=============================
# TENURE GROUP
#=============================
df['TenureGroup'] = pd.cut(
    df['tenure'],
    bins=[0,12,24,48,72],
    labels=[
        "New",
        "Developing",
        "Established",
        "Loyal"
    ],
    include_lowest=True
)

#=============================
# SAVE DATA
#=============================
df.to_csv(OUTPUT_FILE, index=False)

print(f"Shape After: {df.shape}")
print("Data Saved Successfully.")
print(OUTPUT_FILE)


#===============================
# NEW FEATURE VERIFICATION
#===============================
df = pd.read_csv("data/processed/churn_featured.csv")
print(df.columns.tolist())