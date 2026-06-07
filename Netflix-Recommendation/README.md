# 🎬 Netflix Recommendation System

A Netflix-style Content-Based Recommendation System built using Machine Learning, Natural Language Processing (NLP), and Streamlit. The application recommends similar movies and TV series based on genres, directors, actors, writers, and plot descriptions.

---

## 📌 Project Overview

With thousands of movies and TV shows available today, finding relevant content can be challenging. This project addresses that problem by building a recommendation engine that suggests similar content based on movie metadata.

The system uses:

- Content-Based Filtering
- TF-IDF Vectorization
- Cosine Similarity
- IMDb Rating-Based Ranking

Users can select a movie and instantly receive personalized recommendations through an interactive Streamlit web application.

---

## 🚀 Features

✅ Movie and TV Series Recommendations

✅ Content-Based Filtering

✅ NLP-Based Feature Engineering

✅ TF-IDF Vectorization

✅ Cosine Similarity Scoring

✅ IMDb Rating Enhanced Ranking

✅ Interactive Streamlit Interface

✅ Dataset Collected Using OMDb API

---

## 🛠️ Tech Stack

### Programming Language

- Python

### Data Processing

- Pandas
- NumPy

### Machine Learning & NLP

- Scikit-Learn
- TF-IDF Vectorizer
- Cosine Similarity
- NLTK (Porter Stemmer)

### Web Application

- Streamlit

### Data Source

- OMDb API

---

## 📂 Project Structure

```text
Netflix-Recommendation/
│
├── app/
│   └── app.py
│
├── data/
│   ├── Netflix_Dataset.csv
│   └── Netflix_data.csv
│
├── models/
│   ├── tfidf_improved.pkl
│   ├── cosine_similarity_improved.pkl
│   └── movies_improved.pkl
│
├── notebooks/
│   ├── Data_Understanding.ipynb
│   ├── Feature_Engineering.ipynb
│   ├── Recommendation_Model.ipynb
│   └── Model_Improvement.ipynb
│
├── src/
│   ├── collect_movies.py
│   ├── enrich_movies.py
│   ├── merge_data.py
│   └── missing_data.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📊 Dataset Information

The dataset was collected using the OMDb API and contains metadata for movies and TV series.

### Dataset Size

| Metric | Value |
|----------|----------|
| Total Records | 3516 |
| Total Features | 17 |
| Unique IMDb IDs | 3516 |
| Duplicate Records | 0 |

### Key Features

- IMDb ID
- Title
- Genre
- Director
- Writer
- Actors
- Plot
- Runtime
- IMDb Rating
- IMDb Votes
- Country
- Language

---

## 🔍 Exploratory Data Analysis

### Key Findings

- Total Records: 3516
- Average IMDb Rating: 6.44
- Majority Content Type: Movies
- No Duplicate IMDb IDs
- Wide Genre Diversity

### Top Genres

| Genre | Count |
|----------|----------|
| Comedy | 1050 |
| Drama | 846 |
| Action | 765 |
| Animation | 592 |
| Adventure | 563 |

---

## ⚙️ Data Preprocessing

The following preprocessing steps were performed:

### Missing Value Handling

- Filled missing text columns with empty strings
- Replaced missing IMDb ratings with median values

### Feature Engineering

Combined:

- Genre
- Director
- Writer
- Actors
- Plot

into a single feature called:

```text
tags
```

Example:

```text
action adventure scifi christophernolan leonardodicaprio dream extraction technology
```

### Text Processing

- Lowercase conversion
- Space removal from names
- Stemming using Porter Stemmer
- Stop-word removal through TF-IDF

---

## 🧠 Recommendation Engine

### Content-Based Filtering

Movies are recommended based on similarities in:

- Genres
- Directors
- Writers
- Actors
- Plot Descriptions

### TF-IDF Vectorization

Textual movie metadata is transformed into numerical vectors using TF-IDF.

### Cosine Similarity

Pairwise cosine similarity is calculated between all movies.

### Recommendation Formula

Final Recommendation Score:

```text
Final Score =
0.85 × Similarity Score
+
0.15 × Normalized IMDb Rating
```

This ensures that highly similar and highly rated content appears at the top of recommendations.

---

## 🔄 Machine Learning Workflow

```text
Data Collection
        │
        ▼
Data Understanding (EDA)
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Cosine Similarity Matrix
        │
        ▼
Recommendation Engine
        │
        ▼
Streamlit Application
```

---

## 🎯 Sample Recommendations

### Input

```text
A Family Man
```

### Output

```text
Drama Kings
The Family
SuperHero School
Holiday Romance
```

---

## 💻 Running the Project Locally

### Clone Repository

```bash
git clone https://github.com/Abhilash0079/Netflix-Recommendation.git
```

### Navigate to Project

```bash
cd Netflix-Recommendation
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Streamlit App

```bash
streamlit run app/app.py
```

---

## 📸 Application Preview

### Home Page

```text
🎬 Netflix Recommendation System
```

## 📈 Future Enhancements

### Planned Improvements

- Movie Poster Integration
- Netflix-style UI Cards
- Search-Based Recommendations
- Genre Filtering
- Top-Rated Movies Section
- Similarity Score Display
- Explainable Recommendations

### Advanced ML Enhancements

- Collaborative Filtering
- Hybrid Recommendation System
- User-Based Recommendations
- Deep Learning Recommender Models
- Real-Time Recommendation API

---

## 🎓 Skills Demonstrated

### Data Science

- Data Collection
- Exploratory Data Analysis
- Data Cleaning
- Feature Engineering

### Machine Learning

- Recommendation Systems
- Content-Based Filtering
- NLP
- TF-IDF
- Cosine Similarity

### Software Development

- Python Development
- Model Serialization
- Streamlit Deployment
- Git & GitHub

---

## 📚 Learning Outcomes

Through this project, I gained hands-on experience in:

- Building end-to-end recommendation systems
- Working with external APIs
- NLP preprocessing techniques
- Feature engineering for text data
- Similarity-based recommendation algorithms
- Interactive web application development
- Machine Learning project deployment

---

## 👨‍💻 Author

**Abhilash Kumar**

Aspiring Data Scientist and Machine Learning Engineer passionate about solving real-world business problems using data-driven solutions.

### Connect With Me

- LinkedIn: (https://www.linkedin.com/in/abhilash-kumar-824042166/)
- GitHub: (https://github.com/Abhilash0079)

---