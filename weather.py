#
# this script fetches weather data from OpenWeatherMap API using a zip code
# and sends it to a Discord channel using a Discord bot.
#
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

# Base URL for OpenWeatherMap API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(zip_code, country_code="us"):
    """
    Get weather data for a given zip code
    """
    params = {
        "zip": f"{zip_code},{country_code}",
        "appid": API_KEY,
        "units": "imperial"
    }
    
    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and return the relevant weather information as a dictionary
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors
        if response.status_code == 404:
            # 404 probably means invalid zip code
            return {"error": "Invalid zip code"}
        else:
            # Other API errors
            return {"error": f"API error: {str(e)}"}
    except Exception as e:
        # Catch-all for any other errors
        return {"error": f"Error: {str(e)}"}
