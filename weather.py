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
COUNT = 7  # I don't think we're ever changing this so I'm setting it as a constant here

# Base URL for OpenWeatherMap API
CURRENT_WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(zip_code, country_code="us"):
    """
    Get forcast data for a given zip code
    """
    params = {
        "zip": f"{zip_code},{country_code}",
        "appid": API_KEY,
        "units": "imperial"
    }

    try:
        # Make the API request
        response = requests.get(CURRENT_WEATHER_BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses

        # Parse the JSON response
        data = response.json()

        # Extract and return the relevant weather information as a dictionary
        print(data["weather"][0]["icon"])
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


def get_forecast(zip_code, country_code="us"):
    """
    Get weather data for a given zip code
    """
    params = {
        "zip": f"{zip_code},{country_code}",
        "appid": API_KEY,
        "cnt": COUNT,
        # cnt set to 2 for readability, can be adjusted whenever
        "units": "imperial"
    }

    try:
        # Make the API request
        response = requests.get(FORECAST_BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses

        # Parse the JSON response
        data = response.json()

        # Extract and return the relevant weather information as a dictionary
        # data.keys() = ['cod', 'message', 'cnt', 'list', 'city']. The information we're looking for is entirely in 'list'
        # data["list"][0].keys() = ['dt', 'main', 'weather', 'clouds', 'wind', 'visibility', 'pop', 'sys', 'dt_txt']

        # The list key in the first dictionary contains a list of dictionaries for each day. (probably with 0 being today or tomorrow).
        # We will pick out the most relevant parts from inside this list and format them, looping through the list to get each day up to the count.

        # data["list"][1] this accesses the dictionaries of each day
        # The final result should look something like this:
        '''forecast_dict = {"day1" : {"city : ,"temp" : , "feels_like" : , "humidity" : , "description" : ,
            "icon" : ,"wind_speed" :  }, "day2": {etc}}'''

        # Number of days is equal to the cnt parameter
        forecast_dict = {}

        icon_dict = {"01" : "☀️", "02" : "⛅", "03" : "️️☁️", "04" : "️️☁️", "09" : "🌧️", "10" : "🌧️", "11" : "🌩️", "13" : "❄️", "50" : "🌫️"}

        #data["list"][i]['weather'][0]['icon']

        for i in range(params["cnt"]):
            # testing that each dictionary call is correct
            '''print(f"city = {data['city']['name']}")
            print(f"temp = {data["list"][i]['main']['temp']}")
            print(f"feel = {data["list"][i]['main']['feels_like']}")
            print(f"pressure = {data["list"][i]['main']['pressure']}")
            print(f"humidity = {data["list"][i]['main']['humidity']}")

            # for some reason 'weather' is a list with just 1 dictionary inside it, which is why there's an [0]
            print(f"description = {data["list"][i]['weather'][0]['description']}")
            print(f"icon = {icon_dict[data["list"][i]['weather'][0]['icon']]}")
            print(f"wind_speed = {data["list"][i]['wind']['speed']}")
            print(f"icon = {data["list"][i]['weather'][0]['icon'][:2]} icon over")
            '''



            # This should grab all of the data that is needed from the json
            forecast_dict[f"day{i + 1}"] = {"city": data["city"]['name'], "temp_day": data["list"][i]['main']['temp'],
                                            "feels_like_day": data["list"][i]['main']['feels_like'],
                                            "humidity": data["list"][i]['main']['humidity'],
                                            "description": data["list"][i]['weather'][0]['description'],
                                            "icon": icon_dict[data["list"][i]['weather'][0]['icon'][:2]],
                                            "wind_speed": data["list"][i]['wind']['speed']}

        # Return the filled out dictionary
        return forecast_dict

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


# below is used to test functions in terminal/file

#zipcode = input("zip code: ")
#print(get_forecast(zipcode, country_code="us"))

# intended formatting for forecast:
# same as the other one, but just with the extra "day[i]" key at the start and some formatting
