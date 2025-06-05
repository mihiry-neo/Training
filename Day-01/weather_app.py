import logging
import requests
import pandas as pd
import os
import mysql.connector
import pymysql


# Logging Config will create an appending Logging file in "Timestamp-LogLevelName-Message" format. Whenever developer logs in anything, it will be reflected here
logging.basicConfig(
    level=logging.INFO,
    filename = 'weather_app.log',
    filemode = 'a',
    format = '%(asctime)s - %(levelname)s - %(message)s '
)

# Fetching the Weather Info using Weather API
def fetch_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()     
        data = response.json()

        weather = {
            "city":data.get('name',city),
            "country":data.get('sys',{}).get('country','Unknown'),
            "temperature":data.get('main',{}).get('temp',0.0),
            "humidity":data.get('main',{}).get('humidity',0),
            "weather":data.get('weather', [{}])[0].get('main','N/A'),
            "description":data.get('weather',[{}])[0].get('description','N/A')
        }

        logging.info(f"Weather data fetched successfully for {city}")
        return weather
    
    except Exception as e:
        logging.error(f"Faced Error fetching weather data: {e}")
        return None
    

# Saving the Data into a CSV using Pandas
def save_to_csv(data, filename = 'weather_data.csv'):
    try:
        df = pd.DataFrame([data])
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)
        logging.info(f"Weather data saved to {filename}")

    except Exception as e:
        logging.error(f"Faced with an error while saving to csv: {e}")


# Function to insert data from the CSV to MySQL
def insert_into_mysql(data, MYSQL_USER, MYSQL_PASSWORD, host = 'localhost', db='weather_db'):
    try:
        logging.info("Connecting to MySQL...")  
        conn = pymysql.connect(
            host=host,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=db
        )
        logging.info("Connected to MySQL!")

        cursor = conn.cursor()

        insert_query = """
        INSERT INTO weather_info (city,country,temperature,humidity,weather,description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            data['city'],
            data['country'],
            data['temperature'],
            data['humidity'],
            data['weather'],
            data['description']
        )

        cursor.execute(insert_query, values)
        conn.commit()

        logging.info(f"Successfully inserted into MySql for {data['city']}")

        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Faced Error while inserting into MySQL: {e}")


# Performing Aggression Queries

def run_aggregations(MYSQL_USER, MYSQL_PASSWORD, host = 'localhost', db='weather_db'):
    try:
        conn = pymysql.connect(
            host=host,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=db
        )

        cursor = conn.cursor()

        queries = {
            "Total Records":"Select count(*) from weather_info",
            "Average Temperature":"Select avg(temperature) from weather_info",
            "Total Humidity":"Select sum(humidity) from weather_info",
            "Records by Weather":"SELECT weather, COUNT(*) AS total_entries, ROUND(AVG(temperature), 2) AS avg_temp FROM weather_info WHERE weather IS NOT NULL AND weather != '' GROUP BY weather ORDER BY total_entries DESC"
        }

        cursor.execute(queries["Total Records"])
        total = cursor.fetchone()[0]

        cursor.execute(queries["Average Temperature"])
        avg_temp = cursor.fetchone()[0]

        cursor.execute(queries["Total Humidity"])
        total_humidity = cursor.fetchone()[0]

        cursor.execute(queries["Records by Weather"])
        weather_groups = cursor.fetchall()

        logging.info("Aggregation queries executed successfully")

        print("\n=== Summary ===")
        print(f"Total Records: {total}")
        print(f"Average Temperature: {avg_temp:.2f}°C")
        print(f"Total Humidity: {total_humidity}")
        print("\nWeather Group Summary:")
        for weather, count, avg_temp in weather_groups:
            print(f"{weather}: {count} entries, Avg Temp: {avg_temp}°C")


        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Faced Error during aggregation: {e}")



def main():
    API_KEY = 'a3ab736d9b37dcf5e09b86ce4a778435'
    CITY = 'Mumbai'

    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Mihirneo8070*'

    logging.info("=== Weather App Started ===")

    weather = fetch_weather(API_KEY, CITY)
    if weather:
        save_to_csv(weather)
        insert_into_mysql(weather, MYSQL_USER, MYSQL_PASSWORD)
        run_aggregations(MYSQL_USER, MYSQL_PASSWORD)

    logging.info("=== Weather App Finished ===")

main()



