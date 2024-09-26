import unittest
import requests

class TestWeatherAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    # http://127.0.0.1:5000/locations
    def test_locations(self):
        response = requests.get(f"{self.BASE_URL}/locations")
        self.assertEqual(response.status_code, 200)

        # The response is a dictionary with 'data' and 'pagination' fields
        json_data = response.json()
        self.assertIn('data', json_data)  # Check if 'data' field is present
        self.assertIsInstance(json_data['data'], list)  # Check if 'data' is a list

    # http://127.0.0.1:5000/latest-forecast
    def test_latest_forecast(self):
        response = requests.get(f"{self.BASE_URL}/latest-forecast")
        self.assertEqual(response.status_code, 200)

        # The response is a dictionary with 'data' and 'pagination' fields
        json_data = response.json()
        self.assertIn('data', json_data)  # Check if 'data' field is present
        self.assertIsInstance(json_data['data'], list)  # Check if 'data' is a list

    # http://127.0.0.1:5000/average-temperature
    def test_average_temperature(self):
        response = requests.get(f"{self.BASE_URL}/average-temperature")
        self.assertEqual(response.status_code, 200)

        # The response is a dictionary with 'data' and 'pagination' fields
        json_data = response.json()
        self.assertIn('data', json_data)  # Check if 'data' field is present
        self.assertIsInstance(json_data['data'], list)  # Check if 'data' is a list

    # http://127.0.0.1:5000/top-locations?n=3
    def test_top_locations(self):
        response = requests.get(f"{self.BASE_URL}/top-locations?n=3")
        self.assertEqual(response.status_code, 200)

        # The response is a dictionary with 'data' and 'pagination' fields
        json_data = response.json()
        self.assertIn('data', json_data)  # Check if 'data' field is present
        self.assertIsInstance(json_data['data'], list)  # Check if 'data' is a list

if __name__ == "__main__":
    unittest.main()