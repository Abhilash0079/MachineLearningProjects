import pandas as pd
import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#===============================
# LOAD DATA
#===============================
INPUT_FILE = "data/raw/spam_emails.csv"
OUTPUT_FILE = "data/processed/spam_cleaned.csv"

df = pd.read_csv(INPUT_FILE)
print(f"Original Shape: {df.shape}")

#===============================
# TARGET ENCODING
#===============================
df['Category'] = df['Category'].map({
    "ham":0,
    "spam":1
})

#===============================
# NLP OBJECTS
#===============================
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

#===============================
# CLEAN FUNCTION
#===============================
def clean_text(text):
    text = str(text).lower()

    #Remove URLs
    text = re.sub(r"http\S+","",text)

    # Remove Puntuation
    text = text.translate(
        str.maketrans("","",string.punctuation)
    )

    # Remove Digits
    text = re.sub(r"\d+", "", text)

    # Tokenization
    words = text.split()

    # Remove stopwords + lemmatize
    words = [
        lemmatizer.lemmatize(word) for word in words if word not in stop_words
    ]
    return " ".join(words)

#===============================
# CLEAN TEXT
#===============================
df['CleanMessage'] = df['Message'].apply(clean_text)
print("Before:", df.shape)

df["CleanMessage"] = df["CleanMessage"].replace("", pd.NA)
df = df.dropna(subset=["CleanMessage"])

print("After:", df.shape)
#===============================
# SAVE DATA
#===============================
df.to_csv(OUTPUT_FILE, index=False)

print("Saved Successfully.")
print(df.head())


##==================
# TESTING FILE
#====================
print(df.shape)
print(df.columns.tolist())
print(df["Category"].value_counts())
print(df["CleanMessage"].head())