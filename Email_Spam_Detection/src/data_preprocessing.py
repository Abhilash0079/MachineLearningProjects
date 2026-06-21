import pandas as pd
import re
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ===================================
# DOWNLOAD NLTK RESOURCES
# ===================================

nltk.download("stopwords")

# ===================================
# LOAD DATA
# ===================================

INPUT_FILE = "data/raw/emails.csv"
OUTPUT_FILE = "data/processed/email_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print(f"Original Shape: {df.shape}")

# ===================================
# RENAME COLUMNS
# ===================================
df.rename(
    columns={
        "text": "Message",
        "spam": "Category"
    },
    inplace=True
)

# ===================================
# STEMMER & STOPWORDS
# ===================================
ps = PorterStemmer()

stop_words = set(stopwords.words("english"))

# ===================================
# CLEANING FUNCTION
# ===================================
def clean_text(text):
    text = str(text)
    # Lowercase
    text = text.lower()
    # Remove HTML
    text = re.sub(r"<.*?>"," ",text)
    # Remove URLs
    text = re.sub(r"http\S+|www\S+"," ",text)
    # Remove Email IDs
    text = re.sub(r"\S+@\S+"," ",text)
    # Remove Numbers
    text = re.sub(r"\d+"," ",text)
    # Remove Punctuation
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )
    # Tokenization
    words = text.split()
    # Remove Stopwords + Stemming
    words = [
        ps.stem(word)
        for word in words
        if word not in stop_words
    ]
    return " ".join(words)

# ===================================
# APPLY CLEANING
# ===================================

df["CleanMessage"] = df["Message"].apply(clean_text)

# ===================================
# CHECK RESULTS
# ===================================

print(df[[
    "Message",
    "CleanMessage"
]].head())

# ===================================
# SAVE CLEANED DATA
# ===================================
df.to_csv(OUTPUT_FILE,index=False)
print(f"Saved: {OUTPUT_FILE}")
print(f"Final Shape: {df.shape}")