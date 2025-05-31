import requests
import datetime
import os
import json
from dateutil.relativedelta import relativedelta
import sys

# --- Constants and Settings ---
CACHE_FILE = "weather_cache.json"
BASE_API_URL = "https://api.open-meteo.com/v1/forecast"

# Default coordinates for Szczecin, Poland (as per previous context)
DEFAULT_LATITUDE = 53.4289
DEFAULT_LONGITUDE = 14.5530
DEFAULT_TIMEZONE = "Europe/Berlin" # A common timezone for Central Europe

# --- Helper Functions ---

def load_cache():
    """Loads the query cache from a file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Cache file '{CACHE_FILE}' is corrupted or empty. Creating a new one.")
            return {}
        except Exception as e:
            print(f"Error loading cache: {e}")
            return {}
    return {}

def save_cache(cache_data):
    """Saves the query cache to a file."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=4)
    except Exception as e:
        print(f"Error saving cache: {e}")

def get_precipitation_status(precipitation_value):
    """
    Determines the precipitation status based on the value.
    """
    if precipitation_value is None or precipitation_value < 0.0:
        return "I don't know"
    elif precipitation_value > 0.0:
        return f"It will rain (Precipitation: {precipitation_value} mm)"
    else: # precipitation_value == 0.0
        return "It will not rain"

def get_weather_from_api(latitude, longitude, search_date):
    """
    Makes a request to the Open-Meteo API to fetch precipitation data.
    Returns the precipitation value or None in case of an error.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "precipitation_sum",
        "timezone": DEFAULT_TIMEZONE,
        "start_date": search_date.strftime("%Y-%m-%d"),
        "end_date": search_date.strftime("%Y-%m-%d")
    }

    print(f"Requesting API data for {search_date.strftime('%Y-%m-%d')} at ({latitude}, {longitude})...")
    try:
        response = requests.get(BASE_API_URL, params=params, timeout=10)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Check if 'daily' and 'precipitation_sum' exist and have data for the requested date
        if 'daily' in data and 'precipitation_sum' in data['daily'] and len(data['daily']['precipitation_sum']) > 0:
            precipitation = data['daily']['precipitation_sum'][0] # Get the precipitation for the single requested day
            return precipitation
        else:
            print("Warning: Could not find precipitation data in the API response.")
            return None
    except requests.exceptions.Timeout:
        print("Error: API request timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet or API is unreachable.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode API response as JSON.")
        return None
    except Exception as e:
        print(f"Unknown error fetching weather data: {e}")
        return None

# --- Main Program Logic (executes directly) ---

# Load the cache at program start
cache = load_cache()

while True:
    # --- Step 1: Get Date ---
    user_input_date = input(
        f"\nEnter date in YYYY-MM-DD format (e.g., {datetime.date.today().year}-"
        f"{str(datetime.date.today().month).zfill(2)}-"
        f"{str(datetime.date.today().day).zfill(2)}) "
        "or press Enter for tomorrow: "
    ).strip()

    search_date = None
    if not user_input_date:
        # If no date is provided, consider the next day
        search_date = datetime.date.today() + relativedelta(days=1)
        print(f"No date specified. Checking weather for tomorrow: {search_date.strftime('%Y-%m-%d')}")
    else:
        # Validate the user input date format
        try:
            search_date = datetime.datetime.strptime(user_input_date, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
            continue # Ask for date again

    # --- Step 2: Make API Request or Get from Cache ---
    # The cache key now only includes the date, as location is fixed
    cache_key = f"{search_date.strftime('%Y-%m-%d')}"

    precipitation_result = None
    if cache_key in cache:
        # If the date is already in the cache, return the result from the file
        print(f"Result for {search_date.strftime('%Y-%m-%d')} found in cache.")
        precipitation_result = cache[cache_key]
    else:
        # If not in cache, make a request to the API
        precipitation_result = get_weather_from_api(
            DEFAULT_LATITUDE, DEFAULT_LONGITUDE, search_date
        )
        if precipitation_result is not None:
            cache[cache_key] = precipitation_result # Save to cache
            save_cache(cache) # Save cache to file

    # --- Step 3: Determine and Print Precipitation Status ---
    status = get_precipitation_status(precipitation_result)
    print(f"Forecast for {search_date.strftime('%Y-%m-%d')}: {status}")

    # --- Step 4: Continue or Exit ---
    another_check = input("\nDo you want to check another date? (yes/no): ").strip().lower()
    if another_check not in ['yes', 'y']:
        sys.exit(0) # Exit the program
