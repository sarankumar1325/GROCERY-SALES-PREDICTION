from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from api.predict import predict_sales
from api.preprocess import preprocess_data

app = Flask(__name__)
CORS(app)

# Load configuration
if os.path.exists('config.py'):
    app.config.from_object('config')

@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    """Prediction endpoint."""
    try:
        # Get data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Preprocess the input data
        processed_data = preprocess_data(data)
        
        # Make prediction
        prediction, confidence = predict_sales(processed_data)
        
        return jsonify({
            "success": True,
            "prediction": prediction,
            "confidence": confidence
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/predict/form', methods=['POST'])
def predict_form():
    """Form-based prediction endpoint."""
    try:
        # Get form data
        form_data = {key: request.form.get(key) for key in request.form.keys()}
        
        # Preprocess the input data
        processed_data = preprocess_data(form_data)
        
        # Make prediction
        prediction, confidence = predict_sales(processed_data)
        
        return jsonify({
            "success": True,
            "prediction": prediction,
            "confidence": confidence
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/item-types', methods=['GET'])
def get_item_types():
    """Get all unique item types."""
    try:
        item_types = ['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 
                     'Household', 'Baking Goods', 'Snack Foods', 'Frozen Foods', 
                     'Breakfast', 'Health and Hygiene', 'Hard Drinks', 'Canned', 
                     'Breads', 'Starchy Foods', 'Others', 'Seafood']
        
        return jsonify({
            "success": True,
            "item_types": item_types
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/outlet-types', methods=['GET'])
def get_outlet_types():
    """Get all unique outlet types."""
    try:
        outlet_types = ['Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3', 'Grocery Store']
        outlet_sizes = ['Small', 'Medium', 'High']
        outlet_locations = ['Tier 1', 'Tier 2', 'Tier 3']
        
        return jsonify({
            "success": True,
            "outlet_types": outlet_types,
            "outlet_sizes": outlet_sizes,
            "outlet_locations": outlet_locations
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
