# -*- coding: utf-8 -*-
"""Task 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nojtd2o4S9J_9wHSRSWErVICrNBiOoFv

PROJECT 1 : GENERAL EDA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

"""DATASET SELECTION"""

import pandas as pd


try:
    df = pd.read_csv("/content/Global-Superstore.csv", encoding='latin-1')
except UnicodeDecodeError:
    try:
        df = pd.read_csv("/content/Global-Superstore.csv", encoding='cp1252')
    except UnicodeDecodeError:

        print("Error: Could not decode file with common encodings. Please specify the correct encoding.")
        raise

df.head(3)

"""DATA CLEANING"""

# Data Cleaning (Global Superstore)
df.drop_duplicates(inplace=True)
df.drop(columns=['Postal Code'], inplace=True, errors='ignore')
df.fillna(df.median(numeric_only=True), inplace=True)
df

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
df

# Handling outliers using IQR
for col in ["Sales", "Profit", "Discount"]:
    Q1 =  df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

"""STATISTICAL ANALYSIS"""

# Statistical Analysis

print(df.describe())

numerical_df = df.select_dtypes(include=np.number)
print(numerical_df.corr())

"""DATA VISUALIZATION"""

# Data Visualization
plt.figure(figsize=(10, 6))
sns.histplot(df["Sales"], bins=30, kde=True)
plt.title("Sales Distribution")
plt.show

plt.figure(figsize=(10, 6))
sns.boxplot(x=df["Profit"])
plt.title("Profit Boxplot")
plt.show()

plt.figure(figsize=(10, 6))
numerical_df = df.select_dtypes(include=np.number)
sns.heatmap(numerical_df.corr(), annot=True, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()

"""PROJECT 2: SALES PERFORMANCE ANALYSIS

LOAD DATASET
"""

sales_df= pd.read_csv("/content/sales_data.csv")
sales_df.head(3)

"""DATA CLEANING"""

# Data Cleaning (Sales Data)
sales_df.drop_duplicates(inplace=True)
sales_df.fillna(sales_df.median(numeric_only=True), inplace=True)
sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
sales_df

"""EXPLORATORY DATA ANALYSIS"""

#Exploratory Data Analysis
plt.figure(figsize=(12, 6))
sales_df.groupby("Date")["Sales"].sum().plot()
plt.title("Sales Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x=sales_df["Discount"], y=sales_df["Profit"])
plt.title("Discount vs Profit")
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x="Region", y="Sales", data=sales_df)
plt.title("Sales by Region")
plt.xticks(rotation=45)
plt.show()

"""PREDICTIVE MODELLING"""

# Predictive Modeling
X = sales_df[["Profit", "Discount"]]
y = sales_df["Sales"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Model Evaluation
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"R² Score: {r2}")
print(f"Mean Squared Error: {mse}")