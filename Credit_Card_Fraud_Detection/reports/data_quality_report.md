# Data Quality Report

## Project

Credit Card Fraud Detection

## Dataset

fraudTrain.csv

## Analysis Type

Initial Data Understanding (Sample-Based Validation)

---

## Dataset Overview

Rows: 1,296,675

Columns: 23

Missing Values: 0

Duplicate Rows: 0

Fraud Percentage: 0.579%

Legitimate Percentage: 99.421%

---

# Schema Validation

## Numeric Features

* Unnamed: 0
* cc_num
* amt
* zip
* lat
* long
* city_pop
* unix_time
* merch_lat
* merch_long
* is_fraud

## Categorical Features

* merchant
* category
* first
* last
* gender
* street
* city
* state
* job
* trans_num

## Date/Time Features

* trans_date_trans_time
* dob

Observation:

Date-related columns are currently stored as string data types and will require conversion to datetime format during preprocessing.

---

# Missing Value Analysis

## Result

Total Missing Values Found:

0

Observation:

No missing values were detected in the analyzed sample of 5,000 records.

Limitation:

Since only a sample was analyzed, this does not guarantee that the full dataset is free from missing values. Full dataset validation will be performed in a later phase.

---

# Duplicate Record Analysis

Duplicate Rows Found:

0

Observation:

No duplicate records were detected in the analyzed sample.

---

# Target Variable Analysis

Target Column:

is_fraud

Distribution:

Legitimate Transactions (0): 4,978

Fraudulent Transactions (1): 22

Fraud Percentage:

0.44%

Observation:

The dataset is highly imbalanced, which is expected in fraud detection problems.

Potential Impact:

* Accuracy may be misleading.
* Precision, Recall, F1 Score and PR-AUC should be prioritized over Accuracy.
* Resampling techniques such as SMOTE may be required during model training.

---

# Data Quality Issues Identified

## Issue 1

Column:

Unnamed: 0

Observation:

The column appears to be an automatically generated index column and does not contain useful business information.

Action:

Drop the column during preprocessing.

---

## Issue 2

Columns:

* trans_date_trans_time
* dob

Observation:

Both columns are stored as string data types.

Action:

Convert to datetime format and derive additional features such as:

* customer_age
* transaction_hour
* transaction_day
* transaction_month
* transaction_weekday

---

# Preliminary Feature Categories

## Customer Features

* cc_num
* first
* last
* gender
* dob
* city_pop
* job

## Transaction Features

* trans_date_trans_time
* merchant
* category
* amt

## Geographic Features

* city
* state
* lat
* long
* merch_lat
* merch_long

## Target Variable

* is_fraud

---

# Key Findings

1. Dataset structure is valid and readable.
2. No missing values were detected in the sampled records.
3. No duplicate records were detected in the sampled records.
4. Fraudulent transactions represent a very small portion of the data.
5. Datetime columns require preprocessing.
6. The Unnamed: 0 column should be removed.
7. The project will require imbalanced classification techniques.

---

# Next Phase

Exploratory Data Analysis (EDA)

Objectives:

* Analyze transaction amount distributions.
* Study fraud patterns across categories.
* Analyze fraud occurrence by hour.
* Analyze fraud occurrence by state.
* Identify high-risk customer and merchant behaviors.
* Generate business insights for feature engineering.
