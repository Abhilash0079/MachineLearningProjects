import pandas as pd
import joblib
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MaxAbsScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    precision_recall_curve
)

# =====================================
# LOAD TRAIN TEST DATA
# =====================================
X_train = joblib.load("models/X_train.pkl")
X_test = joblib.load("models/X_test.pkl")
y_train = joblib.load("models/y_train.pkl")
y_test = joblib.load("models/y_test.pkl")

#========================================
# SCALING
#========================================
scaler = MaxAbsScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =====================================
# EVALUATION FUNCTION
# =====================================
def evaluate_model(model_name,y_true,y_pred,y_prob):
    return {
        "Model": model_name,
        "Accuracy": round(
            accuracy_score(y_true, y_pred),4
        ),
        "Precision": round(
            precision_score(y_true, y_pred),4
        ),
        "Recall": round(
            recall_score(y_true, y_pred),4
        ),
        "F1 Score": round(
            f1_score(y_true, y_pred),4
        ),
        "ROC AUC": round(
            roc_auc_score(y_true, y_prob),4
        )
    }

results = []

# =====================================
# 1. NAIVE BAYES
# =====================================
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)
nb_pred = nb_model.predict(X_test)
nb_prob = nb_model.predict_proba(X_test)[:,1]

results.append(
    evaluate_model(
        "Naive Bayes",
        y_test,
        nb_pred,
        nb_prob
    )
)

# =====================================
# 2. LOGISTIC REGRESSION
# =====================================
lr_model = LogisticRegression(max_iter=5000, random_state=42)
lr_model.fit(X_train_scaled, y_train)
lr_pred = lr_model.predict(X_test_scaled)
lr_prob = lr_model.predict_proba(X_test_scaled)[:,1]

results.append(
    evaluate_model(
        "Logistic Regression",
        y_test,
        lr_pred,
        lr_prob
    )
)

# =====================================
# 3. LINEAR SVM
# =====================================
svm_model = LinearSVC(max_iter=10000, random_state=42)
svm_model.fit(X_train_scaled, y_train)
svm_pred = svm_model.predict(X_test_scaled)

results.append(
    evaluate_model(
        "Linear SVM",
        y_test,
        svm_pred,
        svm_pred
    )
)

# =====================================
# 4. RANDOM FOREST
# =====================================
rf_model = RandomForestClassifier(n_estimators=200,random_state=42,n_jobs=-1)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_prob = rf_model.predict_proba(X_test)[:,1]

results.append(
    evaluate_model(
        "Random Forest",
        y_test,
        rf_pred,
        rf_prob
    )
)

# =====================================
# RESULTS TABLE
# =====================================
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="ROC AUC",ascending=False)

print("\nModel Comparison:\n")
print(results_df)

# =====================================
# SAVE RESULTS
# =====================================
results_df.to_csv("models/model_results.csv",index=False)

# =====================================
# MODEL DICTIONARY
# =====================================
model_dict = {
    "Naive Bayes": nb_model,
    "Logistic Regression": lr_model,
    "Linear SVM": svm_model,
    "Random Forest": rf_model
}

# =====================================
# BEST MODEL
# =====================================
best_model_name = (results_df.iloc[0]["Model"])
best_model = model_dict[best_model_name]
print(f"\nBest Model: {best_model_name}")

# =====================================
# SAVE BEST MODEL
# =====================================
joblib.dump(nb_model, "models/naive_bayes.pkl")
joblib.dump(lr_model, "models/logistic_regression.pkl")
joblib.dump(svm_model, "models/linear_svm.pkl")
joblib.dump(rf_model, "models/random_forest.pkl")
joblib.dump(best_model,"models/spam_classifier.pkl")
joblib.dump(scaler,"models/scaler.pkl")
print("\nBest Model Saved Successfully")


## Save ROC Curve
lr_model = joblib.load("../models/logistic_regression.pkl")
y_prob = lr_model.predict_proba(X_test_scaled)[:,1]
fpr, tpr, thresholds = roc_curve(y_test, y_prob)

roc_df = pd.DataFrame({
    "FPR": fpr,
    "TPR": tpr
})

roc_df.to_csv(
    "../dashboard/data/roc_curve.csv",
    index=False
)

# Save Precison-Recall Curve
precision, recall, thresholds = precision_recall_curve(
    y_test,
    y_prob
)

pr_df = pd.DataFrame({
    "Precision": precision[:-1],
    "Recall": recall[:-1]
})

pr_df.to_csv(
    "../dashboard/data/pr_curve.csv",
    index=False
)