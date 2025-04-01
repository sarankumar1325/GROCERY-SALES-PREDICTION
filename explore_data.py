import pandas as pd
import numpy as np

# Load the dataset
file_path = 'data/BlinkIT_Grocery_Data.xlsx'
df = pd.read_excel(file_path)

# Print basic information
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values by column:")
print(df.isnull().sum())

# Get basic statistics
print("\nBasic statistics:")
print(df.describe())

# Check column data types
print("\nColumn data types:")
print(df.dtypes)

# Create a processed version
df.to_csv('data/processed_data.csv', index=False)
print("\nProcessed data saved to data/processed_data.csv") 