import requests
import pandas as pd
import time
import os
import sys

API_KEY = "9f362f42a89267dbf2f1dfc219ac893a"  

# Function to fetch weather data
def fetch_weather(city, state):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "state": state,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }
    else:
        return {"city": city, "state": state, "error": "Failed to fetch"}

# Function to append data to final report
def append_to_csv(data, filename="final_report.csv"):
    file_exists = os.path.isfile(filename)
    df = pd.DataFrame([data])
    
    df.to_csv(filename, mode="a", header=not file_exists, index=False)

# Main function
def main(start_index, end_index):
    df = pd.read_csv("cities.csv")
    for index, row in df.iloc[start_index:end_index].iterrows():
        weather_data = fetch_weather(row["city"], row["state"])
        append_to_csv(weather_data)
        time.sleep(1)  # API rate limit handle karne ke liye

if __name__ == "__main__":
    start_index = int(sys.argv[1])
    end_index = int(sys.argv[2])
    main(start_index, end_index)
