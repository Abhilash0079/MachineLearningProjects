import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

#============================
# LOAD DATA
#============================
INPUT_FILE = "data/processed/spam_cleaned.csv"
df = pd.read_csv(INPUT_FILE)
print(f"Shape Before: {df.shape}")

#============================
# CHARACTER COUNT
#============================
df['CharCount'] = df['Message'].apply(lambda x: len(str(x)))

#============================
# WORD COUNT
#============================
df['WordCount'] = df['Message'].apply(lambda x: len(str(x).split()))

#============================
# SENTENCE COUNT
#============================
df['SentenceCount'] = df['Message'].apply(
    lambda x: str(x).count(".") + str(x).count("!") + str(x).count("?")
)

#============================
# AVERAGE WORD LENGTH
#============================
df['AvgWordLength'] = df['Message'].apply(
    lambda x: np.mean(
        [len(word) for word in str(x).split()]
    )if len(str(x).split())>0 else 0
)

#============================
# TF-IDF
#============================
tfidf = TfidfVectorizer(max_features=3000)
X_tfidf = tfidf.fit_transform(df['CleanMessage'])

#============================
# SAVE VECTORIZER
#============================
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")
print("Vectorizer Saved")

#============================
# FEATURE DATAFRAME
#============================
tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=tfidf.get_feature_names_out())

#============================
# COMBINE FEATUREs
#============================
final_df = pd.concat([
    df[[
        'Category',
        "CharCount",
        "WordCount",
        "SentenceCount",
        "AvgWordLength"
    ]],
    tfidf_df
], axis=1)

#============================
# SAVE
#============================
final_df.to_csv("data/processed/spam_featured.csv", index=False)
print(f"Shape After: {final_df.shape}")
print("Feature Engineering Completed")