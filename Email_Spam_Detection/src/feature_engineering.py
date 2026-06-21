import pandas as pd
import numpy as np
import joblib
import string
from sklearn.feature_extraction.text import TfidfVectorizer

# ====================================
# LOAD CLEANED DATA
# ====================================

INPUT_FILE = "data/processed/email_cleaned.csv"
OUTPUT_FILE = "data/processed/email_featured.csv"


df = pd.read_csv(INPUT_FILE)
print(f"Shape Before: {df.shape}")

# ====================================
# EMAIL LENGTH
# ====================================

df["EmailLength"] = df["Message"].apply(lambda x: len(str(x)))

# ====================================
# WORD COUNT
# ====================================

df["WordCount"] = df["Message"].apply(lambda x: len(str(x).split()))

# ====================================
# SENTENCE COUNT
# ====================================

df["SentenceCount"] = df["Message"].apply(
    lambda x:
    str(x).count(".")
    + str(x).count("!")
    + str(x).count("?")
)

# ====================================
# AVERAGE WORD LENGTH
# ====================================

df["AvgWordLength"] = df["Message"].apply(
    lambda x:
    np.mean(
        [len(word)
         for word in str(x).split()]
    )
    if len(str(x).split()) > 0
    else 0
)

# ====================================
# DIGIT COUNT
# ====================================

df["DigitCount"] = df["Message"].apply(
    lambda x: sum(
        c.isdigit()
        for c in str(x)
    )
)

# ====================================
# SPECIAL CHARACTER COUNT
# ====================================

df["SpecialCharCount"] = df["Message"].apply(
    lambda x: sum(
        c in string.punctuation
        for c in str(x)
    )
)

# ====================================
# TF-IDF VECTORIZATION
# ====================================

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1,2)
)

X_tfidf = tfidf.fit_transform(
    df["CleanMessage"]
)

# ====================================
# SAVE TF-IDF VECTORIZER
# ====================================

joblib.dump(tfidf,"models/tfidf_vectorizer.pkl")
print("Vectorizer Saved")

# ====================================
# TF-IDF DATAFRAME
# ====================================

tfidf_df = pd.DataFrame(
    X_tfidf.toarray(),
    columns=tfidf.get_feature_names_out()
)

# ====================================
# COMBINE FEATURES
# ====================================

final_df = pd.concat(
    [
        df[
            [
                "Category",
                "EmailLength",
                "WordCount",
                "SentenceCount",
                "AvgWordLength",
                "DigitCount",
                "SpecialCharCount"
            ]
        ],
        tfidf_df
    ],
    axis=1
)

# ====================================
# SAVE FEATURE DATA
# ====================================
final_df.to_csv(OUTPUT_FILE,index=False)
print(f"Shape After: {final_df.shape}")
print("Feature Engineering Completed")