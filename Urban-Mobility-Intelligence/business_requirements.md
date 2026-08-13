# Business Requirements Document

## Project

**Urban Mobility Intelligence — NYC Taxi Demand & Fare Prediction**

---

# 1. Business Background

Urban taxi services generate large volumes of trip-level data containing information about trip timing, pickup and drop-off locations, distance, duration, fares, passengers, and payment behavior.

Analyzing this data can help transportation stakeholders understand demand patterns, improve resource allocation, estimate fares, and anticipate future demand.

The objective of this project is to transform real-world NYC Yellow Taxi trip data into a data-driven mobility intelligence solution.

---

# 2. Business Problem

Taxi demand is not constant throughout the day or across locations.

Demand can vary significantly based on:

* Time of day
* Day of week
* Weekdays vs weekends
* Location
* Trip distance
* Trip duration
* Seasonal patterns
* Historical demand

Without a data-driven approach, it can be difficult to determine:

* Where taxi demand will be highest
* When demand will increase
* What fare a trip is likely to generate
* Which areas may require greater taxi availability
* How demand will change in the future

---

# 3. Business Objective

The primary objective is to develop an end-to-end Data Science solution capable of:

1. Understanding NYC taxi trip behavior.
2. Predicting taxi fares.
3. Predicting taxi demand levels.
4. Forecasting future taxi demand.
5. Identifying high-demand locations and time periods.
6. Explaining the factors influencing model predictions.
7. Generating actionable business insights.

---

# 4. Primary Business Questions

## Demand

### Q1. When is taxi demand highest?

Analyze demand by:

* Hour
* Day
* Week
* Month
* Weekday/weekend

---

### Q2. Which locations have the highest taxi demand?

Identify high-demand pickup and drop-off zones.

---

### Q3. How does demand vary across different times of the day?

Identify:

* Morning peaks
* Afternoon patterns
* Evening peaks
* Overnight demand

---

### Q4. How does demand differ between weekdays and weekends?

Compare taxi activity across different types of days.

---

# 5. Fare Analysis

### Q5. What factors influence taxi fares?

Investigate relationships between fare and:

* Trip distance
* Trip duration
* Pickup location
* Drop-off location
* Time of day
* Passenger count
* Other relevant trip attributes

---

### Q6. Can the expected fare of a trip be predicted?

Build a regression model that estimates fare using trip characteristics.

---

# 6. Demand Prediction

### Q7. Can we identify periods of low, medium, and high taxi demand?

Create demand categories based on an appropriately defined business methodology.

The classification model should predict:

```text
Low Demand
Medium Demand
High Demand
```

The exact thresholds will be determined from the distribution of the processed data and documented as part of the methodology.

---

# 7. Demand Forecasting

### Q8. Can future taxi demand be forecasted?

Use historical demand patterns to estimate future taxi demand.

Forecasting may be performed at appropriate temporal and geographic levels depending on data volume and model performance.

---

# 8. Geospatial Requirements

The solution should analyze taxi demand by NYC taxi zones.

The analysis should identify:

* High-demand pickup zones
* High-demand drop-off zones
* Demand concentration
* Zone-level demand patterns
* Location-specific fare behavior

---

# 9. Machine Learning Requirements

The project should develop three major machine-learning components.

## 9.1 Fare Prediction

### Problem Type

Regression.

### Target

```text
fare_amount
```

### Expected Output

A predicted taxi fare.

---

## 9.2 Demand Prediction

### Problem Type

Classification.

### Target

A demand category:

```text
Low
Medium
High
```

### Expected Output

Predicted demand level for a given time/location context.

---

## 9.3 Demand Forecasting

### Problem Type

Time-series forecasting / machine-learning forecasting.

### Target

Aggregated taxi demand.

### Expected Output

Forecasted taxi demand for future time periods.

---

# 10. Model Evaluation Requirements

Models must be evaluated using metrics appropriate to the problem.

## Regression

Potential metrics:

* MAE
* RMSE
* R²

Additional metrics may be considered if justified.

---

## Classification

Potential metrics:

* Precision
* Recall
* F1-score
* ROC-AUC
* PR-AUC where appropriate

Accuracy should not be used as the sole model-selection criterion.

---

## Forecasting

Potential metrics:

* MAE
* RMSE
* MAPE / sMAPE where appropriate

The final evaluation methodology will be documented.

---

# 11. Data Requirements

The primary data source must be real-world NYC TLC Yellow Taxi Trip Record Data.

The project will initially use:

```text
2025 Yellow Taxi Trip Records
```

The data is provided in monthly Parquet files.

The first dataset being analyzed is:

```text
yellow_tripdata_2025-01.parquet
```

Supporting taxi-zone information will be obtained from the official TLC source.

---

# 12. Data Quality Requirements

The project must evaluate:

* Missing values
* Duplicate records
* Invalid timestamps
* Invalid trip distances
* Invalid fares
* Invalid passenger counts
* Invalid geographic identifiers
* Extreme outliers
* Data type consistency
* Logical inconsistencies

No data should be removed without defining and documenting the business or technical reason.

---

# 13. Performance Requirements

Because NYC TLC data is large, the project should use memory-efficient processing where appropriate.

The solution should consider:

* Parquet storage
* Column selection
* Data type optimization
* Efficient aggregation
* Chunk-based processing where required
* Avoiding unnecessary copies of large datasets

The solution should be capable of running on a development machine with limited RAM.

---

# 14. Explainability Requirements

The final solution should provide insight into why predictions are generated.

Possible techniques include:

* Feature importance
* Permutation importance
* SHAP

The final approach will depend on the selected models.

---

# 15. Dashboard Requirements

The final dashboard should provide business users with an interactive view of the solution.

The dashboard should include, where appropriate:

### KPIs

* Total trips
* Average fare
* Average trip distance
* Average trip duration
* Peak demand period

### Analysis

* Demand by hour
* Demand by day
* Demand by location
* Fare distribution
* Distance distribution
* Demand trends
* Location-level demand

### Predictions

* Fare prediction
* Demand prediction
* Demand forecast

---

# 16. API Requirements

The final application should expose prediction functionality through an API.

Potential endpoints:

```text
POST /predict-fare
POST /predict-demand
```

The API design will be finalized after the models are developed.

---

# 17. Business Users / Stakeholders

Potential users of the analytical solution include:

* Taxi fleet operators
* Transportation planners
* Mobility companies
* Operations teams
* Business analysts
* Urban transportation researchers
* Data analysts and Data Scientists

---

# 18. Expected Business Benefits

The solution is expected to provide:

### Better demand visibility

Identify when and where taxi demand is highest.

### Better resource planning

Help identify locations and time periods where additional taxi availability may be beneficial.

### Improved fare estimation

Provide data-driven estimates of expected trip fares.

### Better forecasting

Provide visibility into future demand patterns.

### Data-driven decision making

Convert historical transportation data into actionable business insights.

---

# 19. Success Criteria

The project will be considered successful when it can:

* Process the selected NYC TLC data reliably.
* Produce a validated and documented dataset.
* Generate meaningful exploratory insights.
* Build a useful fare prediction model.
* Build a useful demand classification model.
* Build a validated demand forecasting solution.
* Explain important model drivers.
* Provide actionable business recommendations.
* Present the results through an interactive dashboard.
* Expose predictions through an API.
* Be documented and reproducible through GitHub.

---

# 20. Project Constraints

### Hardware

Development will initially be performed on a machine with limited RAM.

### Dataset Size

The NYC TLC dataset is very large and therefore requires efficient data processing.

### Reproducibility

The project should be reproducible from the documented data source and code.

### Scope Control

The project will follow the locked development phases:

```text
Phase 0 → Setup
Phase 1 → Data Understanding
Phase 2 → Data Cleaning
Phase 3 → EDA
Phase 4 → Feature Engineering
Phase 5 → Fare Prediction
Phase 6 → Demand Prediction
Phase 7 → Demand Forecasting
Phase 8 → Explainability & Business Insights
Phase 9 → Dashboard, API & Deployment
Phase 10 → Portfolio & Interview Preparation
```

---

# 21. Out of Scope

The following are outside the initial project scope:

* Real-time taxi GPS tracking
* Real-time ride dispatching
* Dynamic pricing recommendations
* Individual driver performance monitoring
* Customer-level profiling
* Production-scale streaming infrastructure

These may be considered future enhancements but will not be part of the initial implementation.

---

# 22. Final Business Goal

The ultimate goal is to build a portfolio-quality Data Science solution that demonstrates how real-world transportation data can be transformed into:

```text
Raw Data
   ↓
Information
   ↓
Insights
   ↓
Predictions
   ↓
Forecasts
   ↓
Business Decisions
```

The project should demonstrate not only machine-learning skills but also the ability to understand a business problem, work with large real-world datasets, build reliable analytical pipelines, evaluate models correctly, explain results, and communicate findings to stakeholders.
