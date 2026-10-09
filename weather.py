import urllib.request, urllib.parse, urllib.error #For making HTTP requests, encoding URL parameters and catching HTTP errors
import json                         #For parsing JSON responses
from dotenv import load_dotenv      #For loading environment variables from .env file
import os                           #For accessing environment variables

#First we will add the API key to access the OpenWeatherMap API
load_dotenv()

APIKEY = os.getenv("OPENWEATHER_API_KEY")

if not APIKEY:  #Stop early with a clear message instead of failing on the first request
    print("Missing API key. Copy .env.example to .env and set OPENWEATHER_API_KEY.")
    raise SystemExit(1)

serviceurl = 'https://api.openweathermap.org/data/2.5/weather?' #This is the base url to use the API

while True:
    city = input("Enter city (blank to quit): ") #Taking input for city
    if len(city.strip())<1:
        break

    city = city.strip()
    parms = dict()              #Creating a dictionary for parameters
    parms['q'] = city           #Creating the query parameter
    parms['appid'] = APIKEY     #Adding API key to dictionary (required to access the API)
    parms['units'] = 'metric'   #Choosing units

    url = serviceurl + urllib.parse.urlencode(parms)    #Creating the final URL that will give the city's weather information
    print("Retrieving weather for", city)               #Not printing the URL, since it contains the API key

    try:
        uh = urllib.request.urlopen(url)                #Opening the created URL
    except urllib.error.HTTPError as e:                 #The API answers 404 for an unknown city and 401 for a bad key
        if e.code == 404:
            print("City not found, try again.")
        elif e.code == 401:
            print("The API key was rejected. Check OPENWEATHER_API_KEY in your .env file.")
        else:
            print("Request failed with HTTP", e.code)
        continue
    except urllib.error.URLError as e:                  #No internet connection, DNS failure, etc.
        print("Could not reach OpenWeatherMap:", e.reason)
        continue

    data = uh.read().decode()                           #Reading and decoding the opened URL

    try:
        js = json.loads(data) #Parse JSON
    except json.JSONDecodeError:
        js = None

    if not js or 'main' not in js:  #If parsing fails or main is missing, show error
        print("====DOWNLOAD ERROR====")
        print(data)
        continue

#Extracting useful information
    temp = js['main']['temp']
    feels = js['main']['feels_like']
    weather = js['weather'][0]['description']
    wind = js['wind']['speed']
    mintemp = js['main']['temp_min']
    maxtemp = js['main']['temp_max']
#Printing extracted information
    print(f"City: {js['name']}, {js['sys']['country']}")
    print(f"Temperature: {temp}°C (feels like {feels}°C)")
    print(f"Condition: {weather}")
    print(f"Wind speed: {wind} m/s")
    print(f"Max temp: {maxtemp}°C")
    print(f"Min temp: {mintemp}°C")
