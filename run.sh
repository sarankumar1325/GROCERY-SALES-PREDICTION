#!/bin/bash

# Stop script on error
set -e

echo "Grocery Sales Prediction System"
echo "==============================="

# Check for Python
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt
pip install streamlit

# Train model if it doesn't exist
if [ ! -f "backend/model/sales_model.pkl" ]; then
    echo "Training model..."
    cd models
    python train_model.py
    cd ..
fi

# Start backend in background
echo "Starting backend server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

echo "Backend server running with PID $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start frontend
echo "Starting frontend..."
cd frontend
streamlit run streamlit_app.py

# Cleanup when frontend is closed
echo "Stopping backend server..."
kill $BACKEND_PID
