import numpy as np
import pandas as pd
import joblib
import pickle
import os

# Load the model
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'sales_model.pkl')
features_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'features.pkl')

# Cache the model for better performance
_model = None
_features = None

def _load_model():
    """Load the model from disk."""
    global _model, _features
    
    if _model is None:
        try:
            _model = joblib.load(model_path)
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    if _features is None:
        try:
            with open(features_path, 'rb') as f:
                _features = pickle.load(f)
        except Exception as e:
            raise Exception(f"Error loading features: {str(e)}")
    
    return _model, _features

def predict_sales(data):
    """
    Make sales prediction using the loaded model.
    
    Args:
        data (dict or DataFrame): Preprocessed data
        
    Returns:
        tuple: (predicted_sales, confidence_score)
    """
    try:
        # Load model and features
        model, features = _load_model()
        
        # Convert single record to DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Ensure we have all required fields
        required_fields = features['categorical_features'] + features['numerical_features']
        for field in required_fields:
            if field not in df.columns:
                raise Exception(f"Missing required field: {field}")
        
        # Drop the target column if present
        if 'Sales' in df.columns:
            df = df.drop('Sales', axis=1)
        
        # Drop Item Identifier if present (not needed for prediction)
        if 'Item Identifier' in df.columns:
            df = df.drop('Item Identifier', axis=1)
        
        # Make prediction
        predictions = model.predict(df)
        
        # For a single prediction, return the value and confidence
        if len(predictions) == 1:
            # Confidence can be estimated based on the model type
            # For this implementation, we'll use a placeholder value
            # In a real-world scenario, this would be derived from the model's uncertainty
            confidence = 0.85  # 85% confidence
            
            return float(predictions[0]), confidence
        else:
            # For multiple predictions, return the entire array and a confidence for each
            confidences = [0.85] * len(predictions)  # Same confidence for all predictions
            
            return predictions.tolist(), confidences
        
    except Exception as e:
        raise Exception(f"Error in making prediction: {str(e)}")
