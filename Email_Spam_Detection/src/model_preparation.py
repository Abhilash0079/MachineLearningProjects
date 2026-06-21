import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

# =====================================
# LOAD FEATURED DATA
# =====================================
INPUT_FILE = "data/processed/email_featured.csv"
df = pd.read_csv(INPUT_FILE)
print(f"Dataset Shape: {df.shape}")

# =====================================
# FEATURES & TARGET
# =====================================
X = df.drop("Category", axis=1)
y = df["Category"]

print(f"\nFeatures Shape: {X.shape}")
print(f"Target Shape: {y.shape}")

# =====================================
# TRAIN TEST SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTrain-Test Split Completed")

print(f"X_train: {X_train.shape}")
print(f"X_test : {X_test.shape}")

print(f"y_train: {y_train.shape}")
print(f"y_test : {y_test.shape}")

# =====================================
# SAVE FEATURE COLUMNS
# =====================================

joblib.dump(X.columns.tolist(),"models/feature_columns.pkl")
print("\nFeature Columns Saved")

# =====================================
# SAVE TRAIN TEST DATA
# =====================================
joblib.dump(X_train,"models/X_train.pkl")
joblib.dump(X_test,"models/X_test.pkl")
joblib.dump(y_train,"models/y_train.pkl")
joblib.dump(y_test,"models/y_test.pkl")

print("Train/Test Data Saved Successfully")