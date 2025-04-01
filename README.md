# Grocery Sales Prediction

A machine learning project to predict grocery sales based on various product and outlet features using data from BlinkIT.

## Project Overview

This project aims to predict the sales of grocery products in different types of outlets. The system uses machine learning algorithms to analyze historical sales data and identify patterns that influence sales performance.

### Features

- **Sales Prediction**: Predict sales for grocery items based on various features
- **Data Exploration**: Visualize and analyze sales patterns and trends
- **REST API**: Backend Flask API for making predictions
- **User-friendly Interface**: Streamlit dashboard for interactive usage

## Project Structure

```
GrocerySalesPrediction/
├── backend/                # Backend (Flask API)
│   ├── app.py              # Main Flask application
│   ├── model/              # ML model storage
│   │   ├── sales_model.pkl # Trained ML model
│   ├── static/             # Static files
│   ├── templates/          # HTML templates
│   ├── requirements.txt    # Dependencies
│   └── api/                # API endpoints
│       ├── predict.py      # API for making predictions
│       ├── preprocess.py   # Data preprocessing scripts
│       └── utils.py        # Helper functions
│
├── data/                   # Dataset storage
│   ├── BlinkIT_Grocery_Data.xlsx  # Original dataset
│   └── processed_data.csv  # Cleaned dataset
│
├── frontend/               # Frontend (Streamlit)
│   ├── streamlit_app.py    # Streamlit UI
│   ├── static/             # CSS, JS, images
│   ├── templates/          # HTML templates
│   ├── app.js              # Frontend logic
│   └── styles.css          # CSS styles
│
├── models/                 # ML model training
│   ├── train_model.py      # Model training script
│   ├── evaluate.py         # Model evaluation
│   └── model_selection.ipynb  # Model selection notebook
│
├── notebooks/              # Jupyter notebooks
│   ├── eda.ipynb           # Exploratory Data Analysis
│   └── feature_engineering.ipynb  # Feature engineering
│
├── tests/                  # Unit & Integration tests
│   ├── test_api.py         # API testing
│   ├── test_model.py       # ML model testing
│   └── test_ui.py          # Frontend testing
│
├── .gitignore              # Ignore unnecessary files
├── README.md               # Project documentation
├── config.py               # Configuration settings
└── run.sh                  # Script to start the project
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sarankumar1325/GROCERY-SALES-PREDICTION.git
   cd GROCERY-SALES-PREDICTION
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   pip install streamlit
   ```

4. Train the model (if needed):
   ```bash
   cd models
   python train_model.py
   cd ..
   ```

## Usage

### Running the Application

Use the provided run script:

```bash
# On Linux/macOS
chmod +x run.sh
./run.sh

# On Windows (using PowerShell)
# First run: backend
cd backend
python app.py

# Then in a new terminal: frontend
cd frontend
streamlit run streamlit_app.py
```

### Making Predictions

1. Through the Streamlit Interface:
   - Open the Streamlit app at http://localhost:8501
   - Navigate to the "Predict Sales" page
   - Fill in the product and outlet details
   - Click "Predict Sales"

2. Using the REST API:
   - Endpoint: `http://localhost:5000/api/predict`
   - Method: POST
   - Sample payload:
     ```json
     {
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
     ```

## Model Performance

The model achieves over 80% prediction accuracy using a combination of features including:
- Item characteristics (type, weight, visibility, fat content)
- Outlet information (type, location, size, establishment year)
- Item ratings

## Testing

Run tests using pytest:

```bash
# Run API tests
python -m pytest tests/test_api.py

# Run model tests
python -m pytest tests/test_model.py

# Run UI tests
python -m pytest tests/test_ui.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
