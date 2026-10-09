import urllib.request, urllib.parse, urllib.error #For making HTTP requests, encoding URL parameters and catching HTTP errors
import json                         #For parsing JSON responses
from dotenv import load_dotenv      #For loading environment variables from .env file
import os                           #For accessing environment variables

#First we will add the API key to access the OpenWeatherMap API (optional)
load_dotenv()

APIKEY = os.getenv("OPENWEATHER_API_KEY")

OWM_URL = 'https://api.openweathermap.org/data/2.5/weather?'      #OpenWeatherMap current weather (needs a key)
GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search?'       #Open-Meteo city search (no key needed)
METEO_URL = 'https://api.open-meteo.com/v1/forecast?'             #Open-Meteo weather (no key needed)

#Open-Meteo returns a WMO weather code instead of a description, so we translate it
WMO_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "freezing fog",
    51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
    56: "light freezing drizzle", 57: "freezing drizzle",
    61: "light rain", 63: "rain", 65: "heavy rain",
    66: "light freezing rain", 67: "freezing rain",
    71: "light snow", 73: "snow", 75: "heavy snow", 77: "snow grains",
    80: "light rain showers", 81: "rain showers", 82: "violent rain showers",
    85: "light snow showers", 86: "snow showers",
    95: "thunderstorm", 96: "thunderstorm with hail", 99: "thunderstorm with heavy hail",
}


class CityNotFound(Exception):
    pass


def fetch_json(url):
    """Open a URL and return the parsed JSON."""
    uh = urllib.request.urlopen(url, timeout=10)
    return json.loads(uh.read().decode())


def weather_from_openweathermap(city):
    """Current weather from OpenWeatherMap. Used when an API key is set."""
    parms = {'q': city, 'appid': APIKEY, 'units': 'metric'}
    try:
        js = fetch_json(OWM_URL + urllib.parse.urlencode(parms))
    except urllib.error.HTTPError as e:         #The API answers 404 for an unknown city and 401 for a bad key
        if e.code == 404:
            raise CityNotFound(city)
        if e.code == 401:
            raise RuntimeError("The API key was rejected. Check OPENWEATHER_API_KEY in your .env file.")
        raise
    return {
        'city': js['name'], 'country': js['sys']['country'],
        'temp': js['main']['temp'], 'feels': js['main']['feels_like'],
        'condition': js['weather'][0]['description'], 'wind': js['wind']['speed'],
        'min': js['main']['temp_min'], 'max': js['main']['temp_max'],
    }


def weather_from_openmeteo(city):
    """Current weather from Open-Meteo. Free and needs no key, so the app works straight after cloning."""
    geo = fetch_json(GEO_URL + urllib.parse.urlencode({'name': city, 'count': 1}))
    if not geo.get('results'):
        raise CityNotFound(city)
    place = geo['results'][0]

    parms = {
        'latitude': place['latitude'], 'longitude': place['longitude'],
        'current': 'temperature_2m,apparent_temperature,weather_code,wind_speed_10m',
        'daily': 'temperature_2m_max,temperature_2m_min',
        'wind_speed_unit': 'ms', 'timezone': 'auto', 'forecast_days': 1,
    }
    js = fetch_json(METEO_URL + urllib.parse.urlencode(parms))
    now = js['current']
    return {
        'city': place['name'], 'country': place.get('country_code', ''),
        'temp': now['temperature_2m'], 'feels': now['apparent_temperature'],
        'condition': WMO_CODES.get(now['weather_code'], "unknown"), 'wind': now['wind_speed_10m'],
        'min': js['daily']['temperature_2m_min'][0], 'max': js['daily']['temperature_2m_max'][0],
    }


def main():
    if APIKEY:
        get_weather = weather_from_openweathermap
        print("Using OpenWeatherMap.")
    else:
        get_weather = weather_from_openmeteo
        print("No OPENWEATHER_API_KEY found, using Open-Meteo (no key needed).")

    while True:
        city = input("Enter city (blank to quit): ").strip() #Taking input for city
        if len(city) < 1:
            break

        print("Retrieving weather for", city)   #Not printing the URL, since it can contain the API key
        try:
            w = get_weather(city)
        except CityNotFound:
            print("City not found, try again.")
            continue
        except urllib.error.HTTPError as e:
            print("Request failed with HTTP", e.code)
            continue
        except urllib.error.URLError as e:      #No internet connection, DNS failure, etc.
            print("Could not reach the weather service:", e.reason)
            continue
        except (KeyError, IndexError, json.JSONDecodeError):
            print("====DOWNLOAD ERROR==== The weather service sent an unexpected response.")
            continue
        except RuntimeError as e:
            print(e)
            break

        #Printing extracted information
        print(f"City: {w['city']}, {w['country']}")
        print(f"Temperature: {w['temp']}°C (feels like {w['feels']}°C)")
        print(f"Condition: {w['condition']}")
        print(f"Wind speed: {w['wind']} m/s")
        print(f"Max temp: {w['max']}°C")
        print(f"Min temp: {w['min']}°C")


if __name__ == "__main__":
    main()
