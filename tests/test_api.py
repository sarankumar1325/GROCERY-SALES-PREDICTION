import unittest
import json
import sys
import os
import pandas as pd

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app for testing
from backend.app import app

class APITestCase(unittest.TestCase):
    """Test case for the API endpoints."""
    
    def setUp(self):
        """Set up test client before each test."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    def test_predict_missing_data(self):
        """Test prediction endpoint with missing data."""
        response = self.app.post('/api/predict', 
                               data=json.dumps({}),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data.get('success', True))
        self.assertIn('error', data)
    
    def test_predict_valid_data(self):
        """Test prediction endpoint with valid data."""
        # Sample data for prediction
        test_data = {
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
        
        # This test will fail if the model file doesn't exist
        # Skip if not in test environment or model not trained
        model_path = os.path.join('backend', 'model', 'sales_model.pkl')
        if not os.path.exists(model_path):
            self.skipTest("Model file not found, skipping prediction test")
        
        response = self.app.post('/api/predict',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        # Check response structure
        try:
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data.get('success', False))
            self.assertIn('prediction', data)
            self.assertIn('confidence', data)
            
            # Test that prediction is a number
            self.assertIsInstance(data['prediction'], (int, float))
            
            # Test that confidence is a number between 0 and 100
            self.assertIsInstance(data['confidence'], (int, float))
            self.assertGreaterEqual(data['confidence'], 0)
            self.assertLessEqual(data['confidence'], 100)
            
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")
    
    def test_item_types(self):
        """Test item types endpoint."""
        response = self.app.get('/api/item-types')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('success', False))
        self.assertIn('item_types', data)
        self.assertIsInstance(data['item_types'], list)
        self.assertGreater(len(data['item_types']), 0)
    
    def test_outlet_types(self):
        """Test outlet types endpoint."""
        response = self.app.get('/api/outlet-types')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('success', False))
        self.assertIn('outlet_types', data)
        self.assertIn('outlet_sizes', data)
        self.assertIn('outlet_locations', data)
        
        self.assertIsInstance(data['outlet_types'], list)
        self.assertIsInstance(data['outlet_sizes'], list)
        self.assertIsInstance(data['outlet_locations'], list)
        
        self.assertGreater(len(data['outlet_types']), 0)
        self.assertGreater(len(data['outlet_sizes']), 0)
        self.assertGreater(len(data['outlet_locations']), 0)

if __name__ == '__main__':
    unittest.main()
