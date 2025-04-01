# Grocery Sales Prediction

A machine learning project to predict grocery sales using historical data from BlinkIT - a quickcommerce  platform.

## Project Structure

```bash


GrocerySalesPrediction/
├── backend/                # Backend (Flask API)
├── data/                  # Dataset storage
├── frontend/             # Frontend (Streamlit)
├── models/              # ML model training
├── notebooks/          # Jupyter notebooks
└── tests/             # Unit & Integration tests
```

## Setup Instructions

1. Clone the repository
2. Install dependencies:

   ```bash
   # Backend dependencies
   cd backend
   pip install -r requirements.txt

   # Frontend dependencies (if using Streamlit)
   cd ../frontend
   pip install streamlit
   ```

3. Run the application:

   ```bash
   ./run.sh
   ```

## Features

- Machine learning model for sales prediction
- RESTful API using Flask
- Interactive UI using Streamlit
- Comprehensive data analysis and preprocessing
- Unit and integration tests

## Tech Stack

- Backend: Python, Flask
- Frontend: Streamlit
- ML Libraries: scikit-learn, pandas, numpy
- Database: CSV/Excel files

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests
