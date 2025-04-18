import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Create directories if they don't exist
os.makedirs('../backend/model', exist_ok=True)

# Load the data
print("Loading and preprocessing data...")
df = pd.read_csv('../data/processed_data.csv')

# Check for missing values
print(f"Missing values before preprocessing:\n{df.isnull().sum()}")

# Basic data exploration
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

# Fill missing values in Item Weight with the mean
df['Item Weight'].fillna(df['Item Weight'].mean(), inplace=True)

# Check if there are any categorical missing values
categorical_cols = ['Item Fat Content', 'Item Type', 'Outlet Size', 'Outlet Location Type', 'Outlet Type']
for col in categorical_cols:
    if df[col].isnull().sum() > 0:
        # Fill with mode
        df[col].fillna(df[col].mode()[0], inplace=True)

print(f"\nMissing values after filling:\n{df.isnull().sum()}")

# Standardize item fat content
df['Item Fat Content'] = df['Item Fat Content'].replace(['LF', 'low fat', 'Low Fat'], 'Low Fat')
df['Item Fat Content'] = df['Item Fat Content'].replace(['reg', 'Regular'], 'Regular')

# Feature engineering
# Create a feature for Item Identifier prefix (first 2 characters)
df['Item Identifier Prefix'] = df['Item Identifier'].str[:2]

# Define features and target
X = df.drop(['Sales', 'Item Identifier'], axis=1)
y = df['Sales']

# Separate categorical and numerical features
categorical_features = ['Item Fat Content', 'Item Type', 'Outlet Identifier', 
                        'Outlet Size', 'Outlet Location Type', 'Outlet Type', 
                        'Item Identifier Prefix']
numerical_features = ['Outlet Establishment Year', 'Item Visibility', 'Item Weight', 'Rating']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTraining set shape: {X_train.shape}")
print(f"Test set shape: {X_test.shape}")

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ]), numerical_features),
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ]
)

# Create and compare different models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(random_state=42)
}

# Dictionary to store model performance
model_performance = {}

# Set up plot
plt.figure(figsize=(14, 7))
colors = ['blue', 'green', 'red']
i = 0

# Train and evaluate each model
for name, model in models.items():
    print(f"\nTraining {name}...")
    
    # Create pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    # Calculate percentage accuracy (approximation using R²)
    accuracy = max(0, 100 * r2)  # Using R² as a proxy for accuracy
    
    # Store performance
    model_performance[name] = {
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'MAE': mae,
        'Accuracy (%)': accuracy
    }
    
    # Plot predicted vs actual
    plt.subplot(1, 3, i+1)
    plt.scatter(y_test, y_pred, color=colors[i], alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--')
    plt.title(f"{name}\nR² = {r2:.2f}, Accuracy = {accuracy:.2f}%")
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    i += 1

# Save the plot
plt.tight_layout()
plt.savefig('../models/model_comparison.png')
print("Model comparison plot saved to models/model_comparison.png")

# Display model performance
print("\nModel Performance:")
for name, metrics in model_performance.items():
    print(f"\n{name}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

# Select the best model
best_model_name = max(model_performance, key=lambda x: model_performance[x]['R2'])
print(f"\nBest model: {best_model_name} with R² = {model_performance[best_model_name]['R2']:.4f}")

# Fine-tune the best model if it's Random Forest or Gradient Boosting
if best_model_name in ['Random Forest', 'Gradient Boosting']:
    print(f"\nFine-tuning {best_model_name}...")
    
    if best_model_name == 'Random Forest':
        param_grid = {
            'model__n_estimators': [100, 200],
            'model__max_depth': [None, 10, 20],
            'model__min_samples_split': [2, 5]
        }
        model = RandomForestRegressor(random_state=42)
    else:  # Gradient Boosting
        param_grid = {
            'model__n_estimators': [100, 200],
            'model__learning_rate': [0.05, 0.1],
            'model__max_depth': [3, 5]
        }
        model = GradientBoostingRegressor(random_state=42)
    
    # Create pipeline for grid search
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    # Perform grid search
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    # Best parameters
    print(f"Best parameters: {grid_search.best_params_}")
    
    # Evaluate the fine-tuned model
    y_pred = grid_search.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    accuracy = max(0, 100 * r2)
    
    print(f"\nFine-tuned {best_model_name} performance:")
    print(f"  MSE: {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R2: {r2:.4f}")
    print(f"  MAE: {mae:.4f}")
    print(f"  Accuracy (%): {accuracy:.4f}")
    
    # Save the fine-tuned model
    joblib.dump(grid_search, '../backend/model/sales_model.pkl')
    print("Fine-tuned model saved to backend/model/sales_model.pkl")
    
    # Save feature names for later use
    with open('../backend/model/features.pkl', 'wb') as f:
        pickle.dump({
            'categorical_features': categorical_features,
            'numerical_features': numerical_features
        }, f)
else:
    # Save the best model without fine-tuning
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', models[best_model_name])
    ])
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, '../backend/model/sales_model.pkl')
    print("Best model saved to backend/model/sales_model.pkl")
    
    # Save feature names for later use
    with open('../backend/model/features.pkl', 'wb') as f:
        pickle.dump({
            'categorical_features': categorical_features,
            'numerical_features': numerical_features
        }, f)

print("\nModel training complete!")
