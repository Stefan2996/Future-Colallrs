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

# --- Helper Functions (these remain outside the class as they are general utilities) ---

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

# --- NEW CLASS DEFINITION ---
class WeatherForecast:
    def __init__(self, cache_file):
        """
        Initializes the WeatherForecast class, loads data from the cache.
        The cache is stored as a dictionary, where the key is a date string (YYYY-MM-DD).
        """
        self.cache_file = cache_file
        self.data = self._load_cache() # Internal dictionary for storing data

    def _load_cache(self):
        """
        Loads the query cache from a file.
        """
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Cache file '{self.cache_file}' is corrupted or empty. Creating a new one.")
                return {}
            except Exception as e:
                print(f"Error loading cache: {e}")
                return {}
        return {}

    def _save_cache(self):
        """
        Saves the query cache to a file.
        """
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving cache: {e}")

    # --- Special methods (Dunder methods) ---
    def __setitem__(self, date_obj, precipitation_value):
        """
        Allows you to set the weather forecast for a specific date.
        Used as: weather_forecast[date] = value
        date_obj must be a datetime.date object.
        """
        if not isinstance(date_obj, datetime.date):
            raise TypeError("The key must be a datetime.date object.")
        self.data[date_obj.strftime("%Y-%m-%d")] = precipitation_value
        self._save_cache() # Save cache after each change

    def __getitem__(self, date_obj):
        """
        Allows you to get the weather forecast for a specific date.
        Usable as: value = weather_forecast[date]
        date_obj must be a datetime.date object.
        Returns the value or raises KeyError if there is no date.
        """
        if not isinstance(date_obj, datetime.date):
            raise TypeError("The key must be a datetime.date object.")
        return self.data[date_obj.strftime("%Y-%m-%d")]

    def __iter__(self):
        """
        Allows you to iterate over all dates for which the weather forecast is known.
        Returns an iterator over string representations of dates (YYYY-MM-DD).
        """
        return iter(self.data.keys())

    def items(self):
        """
        Returns a generator of tuples in the format (date_obj, weather_value)
        for all saved results.
        date_obj will be a datetime.date object.
        """
        for date_str, weather_value in self.data.items():
            try:
                # Convert the string key back to a datetime.date object
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                yield date_obj, weather_value
            except ValueError:
                print(f"Warning: Invalid date format in cache key: {date_str}. Skipping.")
                continue

# --- Main Program Logic (executes directly) ---

# Load the cache at program start using the new class
weather_forecast = WeatherForecast(CACHE_FILE) # **MODIFIED**

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
    # We now use the WeatherForecast object directly
    precipitation_result = None
    try:
        # Try to get data from cache using __getitem__
        precipitation_result = weather_forecast[search_date] # **MODIFIED**
        print(f"Result for {search_date.strftime('%Y-%m-%d')} found in cache.")
    except KeyError:
        # If not in cache, make a request to the API
        print(f"Result for {search_date.strftime('%Y-%m-%d')} not found in cache. Requesting API.")
        precipitation_result = get_weather_from_api(
            DEFAULT_LATITUDE, DEFAULT_LONGITUDE, search_date
        )
        if precipitation_result is not None:
            # Save to cache using __setitem__
            weather_forecast[search_date] = precipitation_result # **MODIFIED**


    # --- Step 3: Determine and Print Precipitation Status ---
    status = get_precipitation_status(precipitation_result)
    print(f"Forecast for {search_date.strftime('%Y-%m-%d')}: {status}")

    # --- Step 4: Demonstrate new class methods (Optional for testing) ---
    print("\n--- Demonstrating WeatherForecast class methods ---")
    print("All cached dates (using __iter__):")
    for date_str in weather_forecast: # **MODIFIED**
        print(f"  - {date_str}")

    print("All cached items (using items() method):")
    for date_obj, weather_val in weather_forecast.items(): # **MODIFIED**
        print(f"  - Date: {date_obj.strftime('%Y-%m-%d')}, Weather: {get_precipitation_status(weather_val)}") # **MODIFIED**
    print("-------------------------------------------------")


    # --- Step 5: Continue or Exit ---
    another_check = input("\nDo you want to check another date? (yes/no): ").strip().lower()
    if another_check not in ['yes', 'y']:
        sys.exit(0) # Exit the program