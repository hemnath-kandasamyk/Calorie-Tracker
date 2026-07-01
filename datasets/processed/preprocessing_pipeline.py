```python
"""
=========================================================
AI Diet Recommendation System
Data Preprocessing Pipeline

Author : Hemnath KK
Description:
    This script loads the five raw nutrition datasets,
    merges them, cleans the data, and exports a processed
    dataset for machine learning.

Output:
    datasets/processed/nutrition_dataset_v1.csv
=========================================================
"""

# =========================================================
# Step 1 : Import Required Libraries
# =========================================================

import pandas as pd

# =========================================================
# Step 2 : Load Raw Datasets
# =========================================================

print("Loading raw datasets...")

df1 = pd.read_csv("datasets/raw/FOOD-DATA-GROUP1.csv")
df2 = pd.read_csv("datasets/raw/FOOD-DATA-GROUP2.csv")
df3 = pd.read_csv("datasets/raw/FOOD-DATA-GROUP3.csv")
df4 = pd.read_csv("datasets/raw/FOOD-DATA-GROUP4.csv")
df5 = pd.read_csv("datasets/raw/FOOD-DATA-GROUP5.csv")

# =========================================================
# Step 3 : Merge Datasets
# =========================================================

print("Merging datasets...")

df = pd.concat(
    [df1, df2, df3, df4, df5],
    ignore_index=True
)

# =========================================================
# Step 4 : Dataset Overview
# =========================================================

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns)

print("\nInformation")
print(df.info())

# =========================================================
# Step 5 : Remove Unwanted Columns
# =========================================================

print("\nRemoving unnecessary columns...")

df.drop(
    columns=["Unnamed: 0", "Unnamed: 0.1"],
    errors="ignore",
    inplace=True
)

# =========================================================
# Step 6 : Handle Missing Values
# =========================================================

print("Checking missing values...")

print(df.isnull().sum())

# Remove rows containing missing values
df.dropna(inplace=True)

# =========================================================
# Step 7 : Remove Duplicate Records
# =========================================================

print("Checking duplicate rows...")

print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

# =========================================================
# Step 8 : Final Dataset Information
# =========================================================

print("\nFinal Dataset Shape")
print(df.shape)

print("\nFirst Five Rows")
print(df.head())

# =========================================================
# Step 9 : Save Processed Dataset
# =========================================================

output_path = "datasets/processed/nutrition_dataset_v1.csv"

df.to_csv(output_path, index=False)

print("\nProcessed dataset saved successfully.")
print(output_path)

print("\nData preprocessing completed successfully.")
```
