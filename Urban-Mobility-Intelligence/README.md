# 🚕 Urban Mobility Intelligence

## NYC Taxi Demand & Fare Prediction Platform

An end-to-end Data Science project using real-world **NYC Yellow Taxi Trip Record Data** to analyze urban mobility patterns, predict taxi fares, identify demand levels, forecast future taxi demand, and generate actionable business insights.

---

## 📌 Project Overview

Urban transportation generates a large amount of real-world data containing information about trip times, locations, distances, fares, passengers, payment methods, and other trip characteristics.

The objective of this project is to transform this raw transportation data into a complete Data Science solution that can answer questions such as:

* How does taxi demand vary by time and location?
* Which locations experience the highest taxi demand?
* What factors influence taxi fares?
* Can we accurately predict the fare of a taxi trip?
* Can we identify periods of high taxi demand?
* Can future taxi demand be forecasted?
* What insights can help improve taxi availability and urban mobility planning?

The project follows an end-to-end Data Science workflow:

```text
Real-World Data
       ↓
Data Acquisition
       ↓
Data Understanding
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Feature Engineering
       ↓
Machine Learning
       ↓
Model Evaluation
       ↓
Model Explainability
       ↓
Business Insights
       ↓
Dashboard & API
       ↓
Deployment
```

---

# 🎯 Business Objectives

The project focuses on three primary analytical and machine-learning problems.

### 1. Taxi Fare Prediction

Predict the expected fare of a taxi trip using trip characteristics such as:

* Trip distance
* Trip duration
* Pickup location
* Drop-off location
* Passenger count
* Time of day
* Day of week
* Month
* Other relevant trip features

This will be treated as a **regression problem**.

---

### 2. Taxi Demand Prediction

Identify whether a particular time/location combination is expected to experience:

* Low demand
* Medium demand
* High demand

This will be treated as a **classification problem**.

---

### 3. Taxi Demand Forecasting

Forecast future taxi demand using historical trip patterns.

The forecasting component will analyze patterns such as:

* Hourly demand
* Daily demand
* Weekly demand
* Monthly demand
* Location-level demand

---

# 📊 Dataset

The primary dataset is the official:

**NYC Taxi & Limousine Commission (TLC) Yellow Taxi Trip Record Data**

Source:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

The project initially uses **2025 Yellow Taxi Trip Records** distributed as monthly Parquet files.

The first dataset being analyzed is:

```text
yellow_tripdata_2025-01.parquet
```

Additional 2025 monthly datasets will be incorporated after the initial data-quality and processing strategy has been validated.

---

# 🗺️ Supporting Data

The project will also use the official NYC TLC Taxi Zone Lookup information to translate location IDs into meaningful taxi-zone names.

The supporting location data will be stored separately from the primary trip records.

```text
Primary Data
    ↓
Yellow Taxi Trip Records

Supporting Data
    ↓
Taxi Zone Lookup
```

---

# 🧠 Machine Learning Components

## Fare Prediction

Candidate models will include:

* Baseline Regression
* Linear Regression
* Decision Tree Regressor
* Random Forest Regressor
* Gradient Boosting
* XGBoost / other gradient-boosting model where appropriate

Models will be compared using appropriate regression metrics.

---

## Demand Prediction

Candidate classification models may include:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier
* Gradient Boosting
* XGBoost / other gradient-boosting model where appropriate

The final model will be selected based on business-relevant evaluation metrics rather than accuracy alone.

---

## Demand Forecasting

Demand forecasting will be performed using historical aggregated taxi demand.

Depending on the characteristics of the final time-series dataset, we may evaluate:

* Baseline forecasting
* Moving-average approaches
* Statistical forecasting methods
* Machine-learning forecasting models

The final approach will be selected based on validation performance and business usefulness.

---

# 🔬 Feature Engineering

Potential features include:

### Time Features

* Hour
* Day
* Day of week
* Weekend indicator
* Month
* Week of year
* Peak-hour indicator

### Trip Features

* Trip distance
* Trip duration
* Average trip speed
* Passenger count

### Location Features

* Pickup zone
* Drop-off zone
* Pickup demand
* Drop-off demand
* Zone-level historical patterns

### Derived Features

Additional features will be created only after data quality has been validated.

---

# 📈 Exploratory Data Analysis

EDA will investigate:

* Trip volume
* Fare distribution
* Trip distance
* Trip duration
* Demand by hour
* Demand by day
* Demand by month
* Weekday vs weekend behavior
* Pickup-zone demand
* Drop-off-zone demand
* Fare vs distance
* Fare vs duration
* Tip behavior
* Payment patterns
* Outliers and unusual trips

The objective is not only to create visualizations but to identify **business-relevant patterns and relationships**.

---

# 🗺️ Geospatial Analysis

Taxi location IDs will be mapped to NYC taxi zones.

The project will investigate:

* High-demand pickup zones
* High-demand drop-off zones
* Demand concentration
* Zone-level trip patterns
* Peak demand areas
* Spatial differences in fares

Geospatial visualizations will be used to communicate these findings.

---

# 🔎 Model Explainability

The final models will be analyzed to understand which features influence predictions.

Potential techniques include:

* Feature importance
* Permutation importance
* SHAP

The objective is to answer:

> Why did the model make this prediction?

rather than treating the model as a black box.

---

# 💼 Business Insights

The final project will translate analytical and machine-learning results into business recommendations.

Potential questions include:

* When is taxi demand highest?
* Which zones experience the highest demand?
* Which time periods have demand spikes?
* What factors most strongly influence fare?
* Which locations may require additional taxi availability?
* How does demand differ between weekdays and weekends?
* What future demand patterns can be expected?

---

# 🖥️ Dashboard

A Streamlit dashboard will eventually provide an interactive interface for:

* Taxi demand analysis
* Fare prediction
* Demand prediction
* Demand forecasting
* Location-level analysis
* Model insights
* Business KPIs

---

# 🔌 API

A prediction API will eventually expose the trained model for application-level usage.

Potential endpoints will include:

```text
POST /predict-fare
POST /predict-demand
```

The exact API design will be finalized during the deployment phase.

---

# 🏗️ Project Architecture

```text
                         NYC TLC DATA
                              │
                              ▼
                    Data Acquisition
                              │
                              ▼
                   Data Understanding
                              │
                              ▼
                     Data Cleaning
                              │
                              ▼
                           EDA
                              │
                              ▼
                   Feature Engineering
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
          Fare Model    Demand Model    Forecasting
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                     Model Evaluation
                              │
                              ▼
                    Model Explainability
                              │
                              ▼
                      Business Insights
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                Dashboard              API
                    │                   │
                    └─────────┬─────────┘
                              ▼
                         Deployment
```

---

# 📁 Project Structure

```text
urban-mobility-intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│
├── src/
│
├── models/
│
├── reports/
│   └── figures/
│
├── dashboard/
│
├── tests/
│
├── config/
│
├── requirements.txt
├── README.md
├── business_requirements.md
└── .gitignore
```
---

# ⚙️ Technology Stack

### Programming

* Python

### Data Processing

* Pandas
* NumPy
* PyArrow

### Visualization

* Matplotlib
* Seaborn
* Plotly

### Machine Learning

* Scikit-learn
* XGBoost / other appropriate gradient-boosting libraries

### Explainability

* SHAP

### Dashboard

* Streamlit

### API

* FastAPI

### Development

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

# 🖥️ Hardware Consideration

The raw NYC TLC dataset is very large.

Therefore, the project will use memory-efficient data-processing techniques where required, including:

* Parquet format
* Selective column loading
* Chunk-based processing where appropriate
* Data type optimization
* Aggregation before modeling
* Processed datasets for downstream analysis

The complete raw dataset will not be unnecessarily loaded into memory when a more efficient approach is available.

---

# 📏 Model Evaluation

Model evaluation will be based on the specific business problem.

### Regression

Potential metrics:

* MAE
* RMSE
* R²
* MAPE where appropriate

### Classification

Potential metrics:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC where appropriate

### Forecasting

Potential metrics:

* MAE
* RMSE
* MAPE / sMAPE where appropriate

The final metric selection will be justified based on the business objective.

---

# 🚀 Final Deliverables

The completed project will contain:

* Real-world NYC TLC dataset
* Data-quality analysis
* Exploratory analysis
* Feature engineering pipeline
* Fare prediction model
* Demand prediction model
* Demand forecasting model
* Model comparison
* Model explainability
* Business insights
* Interactive dashboard
* Prediction API
* Deployment
* Professional GitHub documentation
* Portfolio description
* Resume bullet points
* Data Science interview questions and answers

---

# 👨‍💻 Author

**Abhilash Kumar**

Software Engineer transitioning into Data Science.

Focus areas:

* Python
* Data Science
* Machine Learning
* Data Analytics
* Backend Development

---

# ⚠️ Project Status

**Current Phase:** Phase 1 — Data Acquisition & Understanding

**Current Dataset:**

```text
NYC Yellow Taxi — January 2025
```

**Current Status:**

🟢 Dataset downloaded
🟢 Project structure created
🟡 Data understanding in progress
⚪ Data cleaning
⚪ EDA
⚪ Feature engineering
⚪ Machine learning
⚪ Forecasting
⚪ Dashboard
⚪ Deployment
