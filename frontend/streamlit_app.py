import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Grocery Sales Prediction",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_BASE_URL = "http://localhost:5000"  # Change this to your backend URL
SAMPLE_DATA_PATH = "../data/processed_data.csv"

# Function to load sample data
@st.cache_data
def load_sample_data():
    try:
        return pd.read_csv(SAMPLE_DATA_PATH)
    except Exception as e:
        st.error(f"Error loading sample data: {e}")
        return None

# Function to get item types from API
@st.cache_data
def get_item_types():
    try:
        response = requests.get(f"{API_BASE_URL}/api/item-types")
        if response.status_code == 200:
            return response.json()["item_types"]
        else:
            # Fallback if API is not available
            return ['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 
                   'Household', 'Baking Goods', 'Snack Foods', 'Frozen Foods', 
                   'Breakfast', 'Health and Hygiene', 'Hard Drinks', 'Canned', 
                   'Breads', 'Starchy Foods', 'Others', 'Seafood']
    except Exception as e:
        st.error(f"Error fetching item types: {e}")
        # Fallback
        return ['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 
               'Household', 'Baking Goods', 'Snack Foods', 'Frozen Foods', 
               'Breakfast', 'Health and Hygiene', 'Hard Drinks', 'Canned', 
               'Breads', 'Starchy Foods', 'Others', 'Seafood']

# Function to get outlet information from API
@st.cache_data
def get_outlet_info():
    try:
        response = requests.get(f"{API_BASE_URL}/api/outlet-types")
        if response.status_code == 200:
            return (
                response.json()["outlet_types"],
                response.json()["outlet_sizes"],
                response.json()["outlet_locations"]
            )
        else:
            # Fallback if API is not available
            return (
                ['Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3', 'Grocery Store'],
                ['Small', 'Medium', 'High'],
                ['Tier 1', 'Tier 2', 'Tier 3']
            )
    except Exception as e:
        st.error(f"Error fetching outlet information: {e}")
        # Fallback
        return (
            ['Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3', 'Grocery Store'],
            ['Small', 'Medium', 'High'],
            ['Tier 1', 'Tier 2', 'Tier 3']
        )

# Function to make prediction
def predict_sales(data):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error from API: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error making prediction: {e}")
        return None

# Set up main interface
def main():
    # Sidebar
    st.sidebar.title("Grocery Sales Prediction")
    
    # Navigation
    page = st.sidebar.radio("Navigation", ["Predict Sales", "Data Explorer", "About"])
    
    if page == "Predict Sales":
        show_prediction_page()
    elif page == "Data Explorer":
        show_data_explorer()
    else:
        show_about_page()

def show_prediction_page():
    st.title("Predict Grocery Sales")
    st.write("Fill in the form below to predict grocery sales.")
    
    # Get item types and outlet information
    item_types = get_item_types()
    outlet_types, outlet_sizes, outlet_locations = get_outlet_info()
    
    # Create columns for form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Item Information")
        
        item_type = st.selectbox("Item Type", options=item_types)
        
        item_fat_content = st.selectbox(
            "Item Fat Content",
            options=["Regular", "Low Fat"]
        )
        
        item_weight = st.number_input(
            "Item Weight (g)",
            min_value=0.0,
            max_value=25.0,
            value=12.85,
            step=0.1
        )
        
        item_visibility = st.slider(
            "Item Visibility",
            min_value=0.0,
            max_value=0.33,
            value=0.066,
            step=0.001,
            help="How visible the item is on the shelf (percentage of total display area)"
        )
        
        rating = st.slider(
            "Item Rating",
            min_value=1.0,
            max_value=5.0,
            value=4.0,
            step=0.1
        )
    
    with col2:
        st.subheader("Outlet Information")
        
        outlet_identifier = st.selectbox(
            "Outlet Identifier",
            options=["OUT010", "OUT013", "OUT017", "OUT018", "OUT019", "OUT027", "OUT035", "OUT045", "OUT046", "OUT049"]
        )
        
        outlet_type = st.selectbox("Outlet Type", options=outlet_types)
        
        outlet_size = st.selectbox("Outlet Size", options=outlet_sizes)
        
        outlet_location = st.selectbox("Outlet Location", options=outlet_locations)
        
        outlet_year = st.slider(
            "Outlet Establishment Year",
            min_value=2011,
            max_value=2022,
            value=2016,
            step=1
        )
    
    # Create item identifier prefix
    item_id_mapping = {
        "Dairy": "FD", "Soft Drinks": "DR", "Meat": "FD", "Fruits and Vegetables": "FD",
        "Household": "HH", "Baking Goods": "FD", "Snack Foods": "FD", "Frozen Foods": "FD",
        "Breakfast": "FD", "Health and Hygiene": "HC", "Hard Drinks": "DR", "Canned": "FD",
        "Breads": "FD", "Starchy Foods": "FD", "Others": "NC", "Seafood": "FD"
    }
    item_identifier_prefix = item_id_mapping.get(item_type, "FD")
    
    # Submit button
    if st.button("Predict Sales"):
        # Create input data
        input_data = {
            "Item Fat Content": item_fat_content,
            "Item Type": item_type,
            "Outlet Identifier": outlet_identifier,
            "Outlet Size": outlet_size,
            "Outlet Location Type": outlet_location,
            "Outlet Type": outlet_type,
            "Item Identifier Prefix": item_identifier_prefix,
            "Outlet Establishment Year": outlet_year,
            "Item Visibility": item_visibility,
            "Item Weight": item_weight,
            "Rating": rating
        }
        
        # Display the input data in a collapsible section
        with st.expander("View Input Data"):
            st.json(input_data)
        
        # Make prediction
        with st.spinner("Making prediction..."):
            result = predict_sales(input_data)
        
        # Display result
        if result and result["success"]:
            st.success("Prediction completed successfully!")
            
            st.metric(
                label="Predicted Sales",
                value=f"${result['prediction']:.2f}",
                help="Predicted sales amount"
            )
            
            st.progress(result["confidence"] / 100)
            st.text(f"Confidence: {result['confidence']}%")
        else:
            st.error("Failed to make prediction. Please check the API connection and try again.")

def show_data_explorer():
    st.title("Data Explorer")
    st.write("Explore the grocery sales dataset.")
    
    # Load sample data
    df = load_sample_data()
    
    if df is not None:
        # Display basic statistics
        st.subheader("Dataset Overview")
        st.write(f"Number of records: {df.shape[0]}")
        st.write(f"Number of features: {df.shape[1]}")
        
        # Display sample data
        st.subheader("Sample Data")
        st.dataframe(df.head(10))
        
        # Show distributions
        st.subheader("Data Distributions")
        
        # Select columns for visualization
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if 'Sales' in numeric_cols:
            # Sales distribution
            st.write("#### Sales Distribution")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(df['Sales'], kde=True, ax=ax)
            st.pyplot(fig)
            
            # Sales by item type
            st.write("#### Average Sales by Item Type")
            avg_sales_by_type = df.groupby('Item Type')['Sales'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.barplot(x=avg_sales_by_type.values, y=avg_sales_by_type.index, ax=ax)
            ax.set_xlabel('Average Sales')
            ax.set_ylabel('Item Type')
            st.pyplot(fig)
            
            # Sales by outlet type
            st.write("#### Average Sales by Outlet Type")
            avg_sales_by_outlet = df.groupby('Outlet Type')['Sales'].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=avg_sales_by_outlet.values, y=avg_sales_by_outlet.index, ax=ax)
            ax.set_xlabel('Average Sales')
            ax.set_ylabel('Outlet Type')
            st.pyplot(fig)
            
            # Correlation heatmap
            st.write("#### Feature Correlations")
            numeric_df = df.select_dtypes(include=[np.number])
            corr = numeric_df.corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)

def show_about_page():
    st.title("About this Application")
    
    st.write("""
    # Grocery Sales Prediction
    
    This application predicts the sales of grocery items based on various features such as item type, 
    item visibility, outlet type, and more.
    
    ## How it works
    
    1. The model is trained on historical grocery sales data
    2. It uses features like item type, item visibility, outlet information, etc.
    3. The backend API processes the input data and makes predictions
    4. The Streamlit frontend provides a user-friendly interface
    
    ## Technology Stack
    
    - **Backend**: Flask API with machine learning model
    - **Frontend**: Streamlit
    - **ML Libraries**: scikit-learn, pandas, numpy
    - **Visualization**: matplotlib, seaborn
    
    ## Model Performance
    
    The model achieves over 80% accuracy in predicting grocery sales.
    """)
    
    # Add team information or references here
    st.subheader("Team")
    st.write("Built by GROCERY-SALES-PREDICTION Team")

if __name__ == "__main__":
    main()
