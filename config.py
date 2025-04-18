import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Application settings
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# API settings
API_PREFIX = '/api'
ALLOWED_ORIGINS = ['*']  # Replace with specific origins in production

# Model settings
MODEL_PATH = os.path.join('backend', 'model', 'sales_model.pkl')
FEATURES_PATH = os.path.join('backend', 'model', 'features.pkl')

# Dataset settings
DATASET_PATH = os.path.join('data', 'BlinkIT_Grocery_Data.xlsx')
PROCESSED_DATA_PATH = os.path.join('data', 'processed_data.csv')

# Streamlit settings
STREAMLIT_PORT = int(os.environ.get('STREAMLIT_PORT', 8501))
STREAMLIT_HOST = os.environ.get('STREAMLIT_HOST', 'localhost')

# Logging settings
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
