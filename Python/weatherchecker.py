"""
weather-checker.py
A terminal-based live weather checker.

Enter a city name and get current conditions: temperature, wind,
humidity, and a plain-language description of the weather. Uses the
free Open-Meteo API, which requires no API key or signup.

Requires: requests
    pip install requests --break-system-packages
"""

import sys

try:
    import requests
except ImportError:
    print("This tool requires the 'requests' package. Install it with:")
    print("    pip install requests --break-system-packages")
    sys.exit(1)

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def geocode_city(city_name):
    """Look up a city name and return (name, country, latitude, longitude), or None."""
    params = {"name": city_name, "count": 5, "language": "en", "format": "json"}

    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Network error while looking up city: {e}")
        return None

    data = response.json()
    results = data.get("results")

    if not results:
        return None

    if len(results) == 1:
        chosen = results[0]
    else:
        print("\nMultiple matches found:")
        for i, r in enumerate(results, start=1):
            region = r.get("admin1", "")
            print(f"{i}. {r['name']}, {region}, {r['country']}")
        while True:
            choice = input(f"Choose 1-{len(results)}: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(results):
                chosen = results[int(choice) - 1]
                break
            print("Invalid choice.")

    return chosen["name"], chosen["country"], chosen["latitude"], chosen["longitude"]

def get_weather(latitude, longitude, use_fahrenheit):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,apparent_temperature",
        "temperature_unit": "fahrenheit" if use_fahrenheit else "celsius",
        "wind_speed_unit": "mph" if use_fahrenheit else "kmh",
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Network error while fetching weather: {e}")
        return None

    return response.json().get("current")

def display_weather(city, country, current, use_fahrenheit):
    temp_unit = "°F" if use_fahrenheit else "°C"
    wind_unit = "mph" if use_fahrenheit else "km/h"

    description = WEATHER_CODES.get(current["weather_code"], "Unknown conditions")

    print(f"\n {city}, {country}")
    print("-" * 40)
    print(f"Conditions:    {description}")
    print(f"Temperature:   {current['temperature_2m']}{temp_unit}")
    print(f"Feels like:    {current['apparent_temperature']}{temp_unit}")
    print(f"Humidity:      {current['relative_humidity_2m']}%")
    print(f"Wind speed:    {current['wind_speed_10m']} {wind_unit}")


def choose_units():
    choice = input("Use Fahrenheit or Celsius? (f/c): ").strip().lower()
    return choice == "f"

def main():
    print("=" * 40)
    print("          LIVE WEATHER CHECKER")
    print("=" * 40)

    use_fahrenheit = choose_units()

    while True:
        city_input = input("\nEnter a city name (or 'q' to quit): ").strip()
        if city_input.lower() == "q":
            print("Goodbye!")
            break

        if not city_input:
            print("Please enter a city name.")
            continue

        location = geocode_city(city_input)
        if location is None:
            print(f"Couldn't find a city matching '{city_input}'.")
            continue

        city, country, lat, lon = location
        current = get_weather(lat, lon, use_fahrenheit)

        if current is None:
            print("Couldn't fetch weather data. Try again.")
            continue

        display_weather(city, country, current, use_fahrenheit)

if __name__ == "__main__":
    main()