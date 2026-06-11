"""
Task 6: Weather Forecast Application — TechnoHacks Internship
=============================================================
Fetches and displays current weather + 5-day forecast
from the OpenWeatherMap API.

Libraries used: requests, json (built-in)
API: OpenWeatherMap (https://openweathermap.org/api)

HOW TO USE:
  1. Get a FREE API key from https://openweathermap.org/api
  2. Replace API_KEY below with your key (or enter when prompted)
  3. Run: python task6_weather_app.py
"""

import requests
import json
from datetime import datetime


# ─── CONFIG ──────────────────────────────────────────────
API_KEY = "398a429c6c8dbc643b5ff3ec42df3da4"   # OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5"
# ─────────────────────────────────────────────────────────


def get_api_key():
    """Get API key from config or prompt the user."""
    if API_KEY != "YOUR_API_KEY_HERE":
        return API_KEY
    print("\n  [INFO]  Get a FREE key at: https://openweathermap.org/api")
    key = input("  Enter your OpenWeatherMap API key: ").strip()
    return key


def fetch_current_weather(city, api_key):
    """Fetch current weather for a city."""
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 401:
            return None, "Invalid API key. Please check your key."
        if response.status_code == 404:
            return None, f"City '{city}' not found. Please check the name."
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.ConnectionError:
        return None, "No internet connection."
    except requests.exceptions.RequestException as e:
        return None, str(e)


def fetch_forecast(city, api_key):
    """Fetch 5-day / 3-hour forecast for a city."""
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "cnt": 40          # max 5 days × 8 readings/day
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def display_current_weather(data, city):
    """Pretty-print current weather data."""
    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    humidity    = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed  = data["wind"]["speed"]
    visibility  = data.get("visibility", 0) // 1000   # meters → km
    country     = data["sys"]["country"]
    sunrise     = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset      = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    print(f"\n{'='*55}")
    print(f"  [LOCATION]  CURRENT WEATHER — {city.upper()}, {country}")
    print(f"{'='*55}")
    print(f"  [TEMP]  Temperature   : {temp:.1f}°C  (Feels like {feels_like:.1f}°C)")
    print(f"  [SKY]  Condition     : {description}")
    print(f"  [HUM]  Humidity      : {humidity}%")
    print(f"  [WIND]  Wind Speed    : {wind_speed} m/s")
    print(f"  [VIS]  Visibility    : {visibility} km")
    print(f"  [SUNRISE]  Sunrise       : {sunrise}")
    print(f"  [SUNSET]  Sunset        : {sunset}")
    print(f"{'='*55}")


def display_forecast(data):
    """Display a daily summary of the 5-day forecast."""
    print(f"\n  [FORECAST]  5-DAY FORECAST")
    print(f"  {'-'*51}")

    # Group by date and pick one reading per day (noon if available)
    daily = {}
    for item in data["list"]:
        date_str = item["dt_txt"].split(" ")[0]
        time_str = item["dt_txt"].split(" ")[1]
        if date_str not in daily or time_str == "12:00:00":
            daily[date_str] = item

    for date_str, item in list(daily.items())[:5]:
        date_obj   = datetime.strptime(date_str, "%Y-%m-%d")
        day_name   = date_obj.strftime("%A, %d %b")
        temp       = item["main"]["temp"]
        desc       = item["weather"][0]["description"].title()
        humidity   = item["main"]["humidity"]
        print(f"  {day_name:<20}  {temp:>5.1f}°C   {desc:<20}  [HUM]{humidity}%")

    print(f"  {'-'*51}\n")


def weather_app():
    """Main application loop."""
    print("\n" + "="*55)
    print("   TASK 6: WEATHER FORECAST APP — TechnoHacks Internship")
    print("   Powered by OpenWeatherMap API")
    print("="*55)

    api_key = get_api_key()

    while True:
        print("\n  Options:")
        print("  [1] Check weather for a city")
        print("  [2] Exit")
        choice = input("\n  Enter choice (1/2): ").strip()

        if choice == "2":
            print("\n  [BYE] Goodbye!\n")
            break

        if choice != "1":
            print("  [WARN]  Invalid choice. Please enter 1 or 2.")
            continue

        city = input("\n  Enter city name: ").strip()
        if not city:
            print("  [WARN]  City name cannot be empty.")
            continue

        print(f"\n  [SEARCH] Fetching weather for '{city}'...")

        # Current weather
        current_data, err = fetch_current_weather(city, api_key)
        if err:
            print(f"\n  [ERROR] Error: {err}")
            continue

        display_current_weather(current_data, city)

        # 5-day forecast
        forecast_data, err = fetch_forecast(city, api_key)
        if forecast_data:
            display_forecast(forecast_data)
        else:
            print(f"  [WARN]  Could not fetch forecast: {err}")

        again = input("  Check another city? (y/n): ").strip().lower()
        if again != "y":
            print("\n  [BYE] Goodbye!\n")
            break


if __name__ == "__main__":
    weather_app()
