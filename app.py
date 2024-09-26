from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Password1994',
            database='weather_data'
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
        raise
    return connection

# For Flask deployment
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Weather API!",
        "endpoints": {
            "/locations": "List all locations",
            "/latest-forecast": "List the latest forecast for each location",
            "/average-temperature": "List the average temperature of the last 3 forecasts for each location",
            "/top-locations?n=<n>": "Get the top n locations based on each available metric where n is a parameter"
        }
    })

# Endpoint to list all locations
@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get pagination parameters from the request, with default values
        page = int(request.args.get('page', 1))  # Default to page 1
        limit = int(request.args.get('limit', 10))  # Default to 10 results per page
        offset = (page - 1) * limit

        # SQL query with LIMIT and OFFSET for pagination
        query = "SELECT * FROM locations LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()

        # Get total number of rows for pagination metadata
        cursor.execute("SELECT COUNT(*) AS total FROM locations")
        total_rows = cursor.fetchone()['total']
        total_pages = (total_rows + limit - 1) // limit  # Calculate total pages

        response = {
            'data': rows,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_rows': total_rows,
            }
        }
        return jsonify(response)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Endpoint to list the latest forecast for each location for every day
@app.route('/latest-forecast', methods=['GET'])
def get_latest_forecast():
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get pagination parameters
        page = int(request.args.get('page', 1))  # Default to page 1
        limit = int(request.args.get('limit', 10))  # Default to 10 results per page
        offset = (page - 1) * limit

        query = """
        SELECT l.location_name, f.forecast_date, f.temperature
        FROM forecasts f
        JOIN locations l ON f.location_id = l.id
        WHERE f.forecast_date = (SELECT MAX(forecast_date) FROM forecasts WHERE location_id = f.location_id)
        ORDER BY l.location_name, f.forecast_date
        LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()

        # Get total number of rows for pagination metadata
        cursor.execute("""
        SELECT COUNT(DISTINCT location_id) AS total
        FROM forecasts
        """)
        total_rows = cursor.fetchone()['total']
        total_pages = (total_rows + limit - 1) // limit

        response = {
            'data': rows,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_rows': total_rows,
            }
        }
        return jsonify(response)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Endpoint to list the average temperature of the last 3 forecasts for each location for every day
@app.route('/average-temperature', methods=['GET'])
def get_average_temperature():
    try:
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get pagination parameters
        page = int(request.args.get('page', 1))  # Default to page 1
        limit = int(request.args.get('limit', 10))  # Default to 10 results per page
        offset = (page - 1) * limit

        # Using a derived table to fetch the last 3 forecasts for each location
        query = """
        SELECT location_name, AVG(temperature) as avg_temperature
        FROM (
            SELECT l.location_name, f.temperature,
                   ROW_NUMBER() OVER (PARTITION BY f.location_id ORDER BY f.forecast_date DESC) as row_num
            FROM forecasts f
            JOIN locations l ON f.location_id = l.id
        ) sub
        WHERE sub.row_num <= 3
        GROUP BY location_name
        LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (limit, offset))
        rows = cursor.fetchall()

        # Get total number of rows for pagination metadata
        cursor.execute("SELECT COUNT(DISTINCT location_id) AS total FROM forecasts")
        total_rows = cursor.fetchone()['total']
        total_pages = (total_rows + limit - 1) // limit

        response = {
            'data': rows,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_rows': total_rows,
            }
        }
        return jsonify(response)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Endpoint to get the top n locations based on the average temperature
@app.route('/top-locations', methods=['GET'])
def get_top_locations():
    try:
        # Get 'n' from the query parameters (e.g., /top-locations?n=3)
        n = request.args.get('n', 10)  # Default to top 10 locations if 'n' is not provided
        if not n.isdigit():
            return jsonify({"error": "Invalid or missing parameter 'n'. Must be a positive integer."}), 400

        n = int(n)
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT l.location_name, AVG(f.temperature) as avg_temperature
        FROM forecasts f
        JOIN locations l ON f.location_id = l.id
        GROUP BY l.location_name
        ORDER BY avg_temperature DESC
        LIMIT %s;
        """
        cursor.execute(query, (n,))
        rows = cursor.fetchall()

        response = {
            'data': rows
        }
        return jsonify(response)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main function to run Flask app
if __name__ == '__main__':
    app.run(debug=True)