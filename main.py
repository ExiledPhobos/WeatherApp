import requests
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

# API credentials
username = "your_username"
password = "your_password"

# API endpoint base URL
base_url = 'https://api.meteomatics.com'

# Defining the date range (7 days from today)
start_date = datetime.now()
end_date = start_date + timedelta(days=7)

# Formatting the dates for the API request
start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

# Defining the locations with latitude, longitude. Feel free to add more if you prefer.
locations = [
    ('Athens', '37.983810', '23.727539'),
    ('Lamia', '38.898857', '22.434397'),
    ('Thessaloniki', '40.640063', '22.944419'),
    ('Heraklion', '35.338735', '25.144213'),
    ('Komotini', '41.120983', '25.401472'),
    ('Ioannina', '39.667919', '20.850618'),
    ('Corfu', '39.624985', '19.921787'),
    ('Mytilene', '39.110514', '26.554750'),
    ('Tripoli', '37.508835', '22.379486'),
    ('Ermoupoli', '37.445982', '24.941050'),
    ('Larissa', '39.639022', '22.419125'),
    ('Patras', '38.246242', '21.735085'),
    ('Kozani', '40.300484', '21.788012'),
    ('Karyes', '40.153011', '24.328826')  # Mt. Athos
]

# Defining the parameters to fetch (temperature at 2 meters in Celsius)
parameters = 't_2m:C'

# Defining the output format (in json)
output_format = 'json'

# Database connection function
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# Function to insert location into the database
def insert_location(connection, location_name, latitude, longitude):
    cursor = connection.cursor()
    select_query = "SELECT id FROM locations WHERE location_name = %s AND latitude = %s AND longitude = %s"
    cursor.execute(select_query, (location_name, latitude, longitude))
    result = cursor.fetchone()

    if result is None:
        insert_query = "INSERT INTO locations (location_name, latitude, longitude) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (location_name, latitude, longitude))
        connection.commit()
        return cursor.lastrowid
    else:
        return result[0]

# Function to insert forecast data into database
def insert_forecast(connection, location_id, forecast_date, temperature):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO forecasts (location_id, forecast_date, temperature)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (location_id, forecast_date, temperature))
    connection.commit()

# Function to fetch weather data and insert into database
def fetch_and_store_weather_data(connection, location_name, lat, lon):
    try:
        # Construct the API URL
        url = f'{base_url}/{start_date_str}--{end_date_str}:P1D/{parameters}/{lat},{lon}/{output_format}'

        # Make the API request with basic authentication
        response = requests.get(url, auth=(username, password))

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            print(f"Data for {location_name} fetched successfully.")
            # For 1st iteration debugging
            # return data

            # Insert location into database
            location_id = insert_location(connection, location_name, lat, lon)

            # Insert each forecast into database
            for date_entry in data['data'][0]['coordinates'][0]['dates']:
                # Convert API datetime format to MySQL compatible format
                forecast_date = date_entry['date']
                forecast_date = datetime.strptime(forecast_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
                temperature = date_entry['value']
                insert_forecast(connection, location_id, forecast_date, temperature)

        else:
            print(f"Failed to fetch data for {location_name}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Connect to MySQL database in Workbench
connection = create_db_connection("localhost", "root", "Password1994", "weather_data")

# Fetch and store data for each location
for location in locations:
    location_name, lat, lon = location
    fetch_and_store_weather_data(connection, location_name, lat, lon)

# Close the database connection
if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")