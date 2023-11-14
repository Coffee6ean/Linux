from unittest import TestCase
from app import app  # Import the Flask app instance, calculated_rate, and error_message

class TestAppServerStatus(TestCase):
    def setUp(self):
        # Set up a test client
        self.app_client = app.test_client()

    def test_get_request_status(self):
        # Make a GET request to the '/' endpoint
        response = self.app_client.get('/')

        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_post_request_status(self):
        # Make a POST request to the '/calculate_rate' endpoint
        response = self.app_client.post('/calculate_rate', json={'firstInput': '1', 'secondInput': '2', 'amountInput': '10'})

        # Check if the status code is 302 (Redirect response)
        self.assertEqual(response.status_code, 302)

class TestAppPage(TestCase):
    def setUp(self):
        # Set up a test client
        self.app_client = app.test_client()

    def test_successful_calculation_flash(self):
        # Make a simulated successful POST request to trigger the success flash message
        response = self.app_client.post('/calculate_rate', json={'firstInput': '1', 'secondInput': '2', 'amountInput': '10'})
        
        # Make a request to the '/' endpoint to check if the success flash message is present in the HTML
        response = self.app_client.get('/')
        
        # Check if the success flash message is present in the HTML
        self.assertIn(b'Calculation successful', response.data)

    def test_error_calculation_flash_invalid_input(self):
        # Make a simulated error POST request with invalid input to trigger the error flash message
        response = self.app_client.post('/calculate_rate', json={'firstInput': '1', 'secondInput': '2', 'amountInput': 'invalid'})
        
        # Make a request to the '/' endpoint to check if the error flash message is present in the HTML
        response = self.app_client.get('/')
        
        # Check if the error flash message is present in the HTML
        self.assertIn(b'could not convert string to float', response.data)

    def test_error_calculation_flash_non_numeric_input(self):
        # Make a simulated error POST request with non-numeric input to trigger the error flash message
        response = self.app_client.post('/calculate_rate', json={'firstInput': 'test', 'secondInput': '2', 'amountInput': '10'})
        
        # Make a request to the '/' endpoint to check if the error flash message is present in the HTML
        response = self.app_client.get('/')
        
        # Check if the error flash message is present in the HTML
        self.assertIn(b'could not convert string to float', response.data)
    
    def test_error_calculation_flash_missing_inputs(self):
        # Make a simulated error POST request with missing input to trigger the error flash message
        response = self.app_client.post('/calculate_rate', json={'firstInput': '1', 'secondInput': '2', 'amountInput': ''})
        
        # Make a request to the '/' endpoint to check if the error flash message is present in the HTML
        response = self.app_client.get('/')
        
        # Check if the error flash message is present in the HTML
        self.assertIn(b'Missing input data', response.data)

    def tearDown(self):
        # Clean up global variables after each test
        app.calculated_rate = None
        app.error_message = None

if __name__ == '__main__':
    unittest.main()
