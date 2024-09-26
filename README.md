# WeatherApp

This project is a weather forecasting app that fetches 7-day weather data for multiple locations using the Meteomatics API. It provides a Flask API with endpoints to list locations, display the latest forecasts, calculate average temperatures, and rank locations based on metrics. The weather data is stored in a MySQL database.

## Features
- Provides a list of all locations stored in the database.
- Displays the most recent forecast for each location.
- Shows the average temperature of the last 3 forecasts for each location.
- Displays the top N locations based on average temperature.

## Prerequisites

1. Ensure Python 3.x is installed.
2. Make sure MySQL is installed and running.
3. Ensure you have `pip` installed to manage Python dependencies.

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/your_username/WeatherApp.git
cd WeatherApp
```

### 2. Set up a virtual environment (Optional, but recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac
.venv\Scripts\activate     # For Windows
```

### 3. Make sure all necessary libraries are installed. Run the following command:
```bash
pip install -r requirements.txt
```

### 4. Setting up the MySQL Database

1. Open MySQL Workbench or any MySQL client. Create a new database called `weather_data`:
```sql
CREATE DATABASE weather_data;
```

2. Import the database structure and data from the provided `Dump20240926.sql` file:
- In MySQL Workbench, go to **Server > Data Import**.
- Choose **Import from Self-Contained File** and select the `Dump20240926.sql` file.
- Make sure to import it into the `weather_data` database.
- Click **Start Import**.

### 5. API Key Setup

1. Get a free API key from [Meteomatics](https://www.meteomatics.com/en/weather-api/).
2. Replace the existing API credentials in your `app.py` with your API key and username:
```python
username = "your_username"
password = "your_password"
```

### 6. Run the Flask app using the following command:
```bash
python app.py
```
The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

- **GET** `/locations`: Lists all available locations.
- **GET** `/latest-forecast`: Displays the latest forecast for each location.
- **GET** `/average-temperature`: Shows the average temperature of the last 3 forecasts for each location.
- **GET** `/top-locations?n=<n>`: Returns the top `n` locations based on the average temperature.

## To run unit tests for the application, use:
```bash
python -m unittest test_app.py
```

## License
This project is licensed under the MIT License.
```