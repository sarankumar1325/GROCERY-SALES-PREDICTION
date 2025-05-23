import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle

# Load the test data
print("Loading test data...")
df = pd.read_csv('../data/processed_data.csv')

# Load features
with open('../backend/model/features.pkl', 'rb') as f:
    features = pickle.load(f)

categorical_features = features['categorical_features']
numerical_features = features['numerical_features']

# Create item identifier prefix if it doesn't exist
if 'Item Identifier Prefix' not in df.columns:
    df['Item Identifier Prefix'] = df['Item Identifier'].str[:2]

# Standardize item fat content
df['Item Fat Content'] = df['Item Fat Content'].replace(['LF', 'low fat', 'Low Fat'], 'Low Fat')
df['Item Fat Content'] = df['Item Fat Content'].replace(['reg', 'Regular'], 'Regular')

# Split features and target
X = df.drop(['Sales', 'Item Identifier'], axis=1)
y = df['Sales']

# Load the model
print("Loading model...")
model = joblib.load('../backend/model/sales_model.pkl')

# Make predictions
print("Making predictions...")
y_pred = model.predict(X)

# Calculate metrics
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)
accuracy = max(0, 100 * r2)  # Using R² as a proxy for accuracy

print("\nModel Evaluation Metrics:")
print(f"  MSE: {mse:.4f}")
print(f"  RMSE: {rmse:.4f}")
print(f"  R2: {r2:.4f}")
print(f"  MAE: {mae:.4f}")
print(f"  Accuracy (%): {accuracy:.4f}")

# Plot actual vs predicted
plt.figure(figsize=(10, 6))
plt.scatter(y, y_pred, alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--')
plt.title(f"Actual vs Predicted Sales\nR² = {r2:.2f}, Accuracy = {accuracy:.2f}%")
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.tight_layout()
plt.savefig('../models/model_evaluation.png')
print("Evaluation plot saved to models/model_evaluation.png")

# Feature importance (if available)
try:
    # Try to extract feature importance
    if hasattr(model, 'named_steps') and hasattr(model.named_steps['model'], 'feature_importances_'):
        # For pipeline with feature importances
        importances = model.named_steps['model'].feature_importances_
        
        # Get feature names after preprocessing
        preprocessor = model.named_steps['preprocessor']
        feature_names = []
        
        # Extract transformed feature names
        for name, transformer, features in preprocessor.transformers_:
            if hasattr(transformer, 'get_feature_names_out'):
                feature_names.extend(transformer.get_feature_names_out(features))
            else:
                feature_names.extend(features)
        
        # Create feature importance dataframe
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Importance', y='Feature', data=importance_df.head(20))
        plt.title('Top 20 Feature Importance')
        plt.tight_layout()
        plt.savefig('../models/feature_importance.png')
        print("Feature importance plot saved to models/feature_importance.png")
        
    elif hasattr(model, 'best_estimator_') and hasattr(model.best_estimator_.named_steps['model'], 'feature_importances_'):
        # For GridSearchCV with pipeline
        importances = model.best_estimator_.named_steps['model'].feature_importances_
        
        # Get feature names after preprocessing
        preprocessor = model.best_estimator_.named_steps['preprocessor']
        feature_names = []
        
        # Extract transformed feature names
        for name, transformer, features in preprocessor.transformers_:
            if hasattr(transformer, 'get_feature_names_out'):
                feature_names.extend(transformer.get_feature_names_out(features))
            else:
                feature_names.extend(features)
        
        # Create feature importance dataframe
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Importance', y='Feature', data=importance_df.head(20))
        plt.title('Top 20 Feature Importance')
        plt.tight_layout()
        plt.savefig('../models/feature_importance.png')
        print("Feature importance plot saved to models/feature_importance.png")
except Exception as e:
    print(f"Could not extract feature importance: {e}")

print("\nModel evaluation complete!")
