import pandas as pd
import numpy as np
import os
import json
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_unique_values(df, column):
    """
    Get unique values for a given column.
    
    Args:
        df (DataFrame): The dataframe
        column (str): Column name
        
    Returns:
        list: List of unique values
    """
    try:
        if column in df.columns:
            return df[column].unique().tolist()
        else:
            return []
    except Exception as e:
        logger.error(f"Error getting unique values for {column}: {str(e)}")
        return []

def get_sample_data():
    """
    Get sample data for testing.
    
    Returns:
        dict: Sample data record
    """
    return {
        "Item Fat Content": "Low Fat",
        "Item Type": "Fruits and Vegetables",
        "Outlet Identifier": "OUT049",
        "Outlet Size": "Medium",
        "Outlet Location Type": "Tier 1",
        "Outlet Type": "Supermarket Type1",
        "Item Identifier Prefix": "FD",
        "Outlet Establishment Year": 2016,
        "Item Visibility": 0.066,
        "Item Weight": 12.85,
        "Rating": 4.0
    }

def validate_input(data, required_fields):
    """
    Validate input data against required fields.
    
    Args:
        data (dict): Input data
        required_fields (list): List of required field names
        
    Returns:
        tuple: (valid, error_message)
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, ""

def format_prediction(prediction, confidence):
    """
    Format prediction output.
    
    Args:
        prediction (float): Predicted sales value
        confidence (float): Confidence level
        
    Returns:
        dict: Formatted prediction output
    """
    return {
        "predicted_sales": round(prediction, 2),
        "confidence": round(confidence * 100, 2),
        "formatted_sales": f"${prediction:.2f}",
        "confidence_level": get_confidence_level(confidence)
    }

def get_confidence_level(confidence):
    """
    Convert numerical confidence to descriptive level.
    
    Args:
        confidence (float): Confidence value (0-1)
        
    Returns:
        str: Confidence level description
    """
    if confidence >= 0.9:
        return "Very High"
    elif confidence >= 0.8:
        return "High"
    elif confidence >= 0.7:
        return "Moderate"
    elif confidence >= 0.6:
        return "Low"
    else:
        return "Very Low"
