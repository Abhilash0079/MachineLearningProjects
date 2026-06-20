import pandas as pd
import joblib
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

#========================
# LOAD DATA
#========================
X_train = joblib.load("models/X_train.pkl")
X_test = joblib.load("models/X_test.pkl")
y_train = joblib.load("models/y_train.pkl")
y_test = joblib.load("models/y_test.pkl")

#========================
# EVALUATION FUNCTION
#========================
def evaluate_model(model_name, y_true, y_pred, y_prob):
    return {
        "Model": model_name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1 Score": f1_score(y_true, y_pred),
        "ROC AUC": roc_auc_score(y_true, y_prob)
    }

results = []

#=============================
# 1. Multinomial Naive Bayes
#=============================
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

#=============================
# 2. Logistic Regression
#=============================
lr_model = LogisticRegression(max_iter=5000)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_prob = lr_model.predict_proba(X_test)[:,1]

results.append(
    evaluate_model(
        "Logistic Regression",
        y_test,
        lr_pred, 
        lr_prob
    )
)

#=============================
# 3. Linear SVM
#=============================
svm_model = LinearSVC()
svm_model.fit(X_train, y_train)
svm_pred = svm_model.predict(X_test)

results.append(
    evaluate_model(
        "Linear SVM",
        y_test,
        svm_pred,
        svm_pred
    )
)

#=============================
# 4. Random Forest
#=============================
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
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

#====================
# RESULT TABLE
#====================
results_df = pd.DataFrame(results)
#=================================
# MODEL DICTIONARY
#=================================

model_dict = {
    "Naive Bayes": nb_model,
    "Logistic Regression": lr_model,
    "Linear SVM": svm_model,
    "Random Forest": rf_model
}

#=================================
# FIND BEST MODEL
#=================================
best_model_name = results_df.sort_values(by="ROC AUC", ascending=False).iloc[0]["Model"]
best_model = model_dict[best_model_name]
print(f"Best Model: {best_model_name}")

#=======================
# SAVE BEST MODEL
#=======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "spam_classifier.pkl"
)
joblib.dump(best_model, MODEL_PATH)
print(f"Model saved at: {MODEL_PATH}")