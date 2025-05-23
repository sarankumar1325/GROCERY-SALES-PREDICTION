import unittest
import sys
import os
import pandas as pd
import numpy as np
import joblib
import pickle

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ModelTestCase(unittest.TestCase):
    """Test case for the ML model."""
    
    def setUp(self):
        """Set up test data before each test."""
        # Define paths
        self.model_path = os.path.join('backend', 'model', 'sales_model.pkl')
        self.features_path = os.path.join('backend', 'model', 'features.pkl')
        self.data_path = os.path.join('data', 'processed_data.csv')
        
        # Skip tests if data or model don't exist
        if not os.path.exists(self.data_path):
            self.skipTest("Processed data file not found")
        
        if not os.path.exists(self.model_path) or not os.path.exists(self.features_path):
            self.skipTest("Model or features file not found")
        
        # Load data for testing
        self.data = pd.read_csv(self.data_path)
        
        # Load model and features
        try:
            self.model = joblib.load(self.model_path)
            with open(self.features_path, 'rb') as f:
                self.features = pickle.load(f)
        except Exception as e:
            self.skipTest(f"Error loading model: {str(e)}")
    
    def test_model_exists(self):
        """Test that model file exists."""
        self.assertTrue(os.path.exists(self.model_path))
    
    def test_features_exists(self):
        """Test that features file exists."""
        self.assertTrue(os.path.exists(self.features_path))
    
    def test_model_can_predict(self):
        """Test that model can make predictions."""
        # Skip if no data
        if self.data.empty:
            self.skipTest("No data for testing")
        
        # Select a random sample for prediction
        sample = self.data.sample(1).copy()
        
        # Prepare input data
        X = sample.drop(['Sales', 'Item Identifier'], axis=1, errors='ignore')
        
        # Make prediction
        try:
            prediction = self.model.predict(X)
            self.assertIsInstance(prediction, np.ndarray)
            self.assertEqual(len(prediction), 1)
            self.assertIsInstance(prediction[0], (int, float))
        except Exception as e:
            self.fail(f"Model prediction failed: {str(e)}")
    
    def test_feature_importance(self):
        """Test that feature importance can be extracted (if applicable)."""
        # Skip for non-tree-based models
        if not hasattr(self.model, 'named_steps') or not hasattr(self.model.named_steps.get('model', {}), 'feature_importances_'):
            if not hasattr(self.model, 'best_estimator_') or not hasattr(self.model.best_estimator_.named_steps.get('model', {}), 'feature_importances_'):
                self.skipTest("Model doesn't support feature importance")
        
        try:
            # Try to extract feature importance
            if hasattr(self.model, 'named_steps') and hasattr(self.model.named_steps.get('model', {}), 'feature_importances_'):
                importances = self.model.named_steps['model'].feature_importances_
            elif hasattr(self.model, 'best_estimator_') and hasattr(self.model.best_estimator_.named_steps.get('model', {}), 'feature_importances_'):
                importances = self.model.best_estimator_.named_steps['model'].feature_importances_
            
            self.assertIsInstance(importances, np.ndarray)
            self.assertGreater(len(importances), 0)
            
            # Test that feature importances sum to approximately 1 (tree-based models)
            self.assertAlmostEqual(np.sum(importances), 1.0, delta=0.01)
        except Exception as e:
            self.fail(f"Feature importance extraction failed: {str(e)}")
    
    def test_model_prediction_range(self):
        """Test that model predictions are within a reasonable range."""
        # Skip if no data
        if self.data.empty:
            self.skipTest("No data for testing")
        
        # Sales should be positive values
        # Prepare input data (use 10 samples)
        samples = self.data.sample(min(10, len(self.data))).copy()
        X = samples.drop(['Sales', 'Item Identifier'], axis=1, errors='ignore')
        
        # Make predictions
        try:
            predictions = self.model.predict(X)
            
            # Check predictions are positive
            self.assertTrue(np.all(predictions > 0))
            
            # Check predictions are within a reasonable range
            # (based on typical grocery sales values)
            self.assertTrue(np.all(predictions < 500))  # Assuming max sale value
        except Exception as e:
            self.fail(f"Model prediction range test failed: {str(e)}")
    
    def test_required_features(self):
        """Test that features file contains expected features."""
        # Check required feature groups
        self.assertIn('categorical_features', self.features)
        self.assertIn('numerical_features', self.features)
        
        # Check specific important features
        all_features = self.features['categorical_features'] + self.features['numerical_features']
        
        important_features = [
            'Item Type', 'Outlet Type', 'Item Visibility', 'Item Weight'
        ]
        
        for feature in important_features:
            self.assertIn(feature, all_features)

if __name__ == '__main__':
    unittest.main()
