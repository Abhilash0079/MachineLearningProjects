import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

#=========================
# LOAD DATA
#=========================
INPUT_FILE = "data/processed/spam_featured.csv"
df = pd.read_csv(INPUT_FILE)
print(f"Shape: {df.shape}")

#=========================
# TARGET
#=========================
X = df.drop("Category", axis=1)
y = df['Category']

print(f"\nFeatures Shape: {X.shape}")
print(f"Target Shape: {y.shape}")

#=========================
# TRAIN TEST SPLIT
#=========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
print(f"\nX Train: {X_train.shape}")
print(f"X Test: {X_test.shape}")

#=========================
# SAVE FEATURE COLUMNS
#=========================
joblib.dump(X.columns.tolist(),"models/feature_columns.pkl")
print("Feature Columns Saved")

#=========================
# SAVE SPLITS
#=========================
joblib.dump(X_train, "models/X_train.pkl", compress=9)
joblib.dump(X_test, "models/X_test.pkl", compress=9)

joblib.dump(y_train, "models/y_train.pkl", compress=9)
joblib.dump(y_test, "models/y_test.pkl", compress=9)

print("Train/Test Data Saved")