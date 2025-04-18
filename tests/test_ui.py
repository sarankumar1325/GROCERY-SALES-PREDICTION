import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class UITestCase(unittest.TestCase):
    """Basic test case for the UI files."""
    
    def setUp(self):
        """Set up before each test."""
        # Define paths to check
        self.streamlit_app_path = os.path.join('frontend', 'streamlit_app.py')
        self.template_path = os.path.join('backend', 'templates', 'index.html')
    
    def test_streamlit_app_exists(self):
        """Test that Streamlit app file exists."""
        self.assertTrue(os.path.exists(self.streamlit_app_path))
    
    def test_template_exists(self):
        """Test that HTML template exists."""
        self.assertTrue(os.path.exists(self.template_path))
    
    def test_streamlit_app_content(self):
        """Test that Streamlit app file has required content."""
        with open(self.streamlit_app_path, 'r') as f:
            content = f.read()
            # Check for required imports
            self.assertIn('import streamlit as st', content)
            # Check for main function
            self.assertIn('def main()', content)
            # Check for prediction code
            self.assertIn('predict_sales', content)
    
    def test_template_content(self):
        """Test that HTML template has required content."""
        with open(self.template_path, 'r') as f:
            content = f.read()
            # Check for basic HTML structure
            self.assertIn('<!DOCTYPE html>', content)
            self.assertIn('</html>', content)
            # Check for API documentation
            self.assertIn('API Documentation', content)
            # Check for test prediction functionality
            self.assertIn('Test Prediction', content)

if __name__ == '__main__':
    unittest.main()
