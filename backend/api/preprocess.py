import pandas as pd
import numpy as np

def preprocess_data(data):
    """
    Preprocess input data for prediction.
    
    Args:
        data (dict): Input data containing features
        
    Returns:
        dict: Preprocessed data ready for prediction
    """
    try:
        # Convert to DataFrame if it's a dictionary
        if isinstance(data, dict):
            # If single record, convert to DataFrame
            df = pd.DataFrame([data])
        else:
            # If already a DataFrame, use it directly
            df = data.copy()
        
        # Standard preprocessing steps
        
        # Fill missing values for numeric fields
        numeric_fields = ['Item Weight', 'Item Visibility', 'Outlet Establishment Year', 'Rating']
        for field in numeric_fields:
            if field in df.columns and df[field].isnull().any():
                # Use default values from training
                default_values = {
                    'Item Weight': 12.85,        # Mean from training
                    'Item Visibility': 0.066,     # Mean from training
                    'Outlet Establishment Year': 2016,  # Mode from training
                    'Rating': 4.0                # Median from training
                }
                df[field].fillna(default_values[field], inplace=True)
        
        # Convert data types for numeric fields
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors='coerce')
                # Replace NaN with default values
                if df[field].isnull().any():
                    default_values = {
                        'Item Weight': 12.85,
                        'Item Visibility': 0.066,
                        'Outlet Establishment Year': 2016,
                        'Rating': 4.0
                    }
                    df[field].fillna(default_values[field], inplace=True)
        
        # Standardize categorical values
        # Item Fat Content
        if 'Item Fat Content' in df.columns:
            df['Item Fat Content'] = df['Item Fat Content'].replace(['LF', 'low fat', 'Low Fat'], 'Low Fat')
            df['Item Fat Content'] = df['Item Fat Content'].replace(['reg', 'Regular'], 'Regular')
        
        # Create Item Identifier Prefix if Item Identifier is provided
        if 'Item Identifier' in df.columns and 'Item Identifier Prefix' not in df.columns:
            df['Item Identifier Prefix'] = df['Item Identifier'].str[:2]
        
        # Fill missing categorical values
        categorical_fields = ['Item Fat Content', 'Item Type', 'Outlet Size', 
                              'Outlet Location Type', 'Outlet Type', 'Item Identifier Prefix']
        
        default_values = {
            'Item Fat Content': 'Regular',
            'Item Type': 'Fruits and Vegetables',
            'Outlet Size': 'Medium',
            'Outlet Location Type': 'Tier 2',
            'Outlet Type': 'Supermarket Type1',
            'Item Identifier Prefix': 'FD'
        }
        
        for field in categorical_fields:
            if field in df.columns and df[field].isnull().any():
                df[field].fillna(default_values[field], inplace=True)
        
        # Return as dictionary for single record or DataFrame for multiple records
        if len(df) == 1:
            return df.iloc[0].to_dict()
        else:
            return df
        
    except Exception as e:
        raise Exception(f"Error in preprocessing data: {str(e)}")
