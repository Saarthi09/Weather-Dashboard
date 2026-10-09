# Weather CLI

A command-line weather app in Python. Type a city and get its current weather. **It works straight after cloning, with no API key needed.**

```
$ python weather.py
No OPENWEATHER_API_KEY found, using Open-Meteo (no key needed).
Enter city (blank to quit): Toronto
Retrieving weather for Toronto
City: Toronto, CA
Temperature: 12.1°C (feels like 10.4°C)
Condition: light rain
Wind speed: 4.2 m/s
Max temp: 14.0°C
Min temp: 9.8°C
Enter city (blank to quit): Atlantis
Retrieving weather for Atlantis
City not found, try again.
```

## Features

- Current temperature and "feels like" temperature in °C, a weather description, wind speed, and the day's min/max
- Two data sources behind one interface:
  - **[Open-Meteo](https://open-meteo.com/)** by default: free, no sign-up, no key
  - **[OpenWeatherMap](https://openweathermap.org/current)** when you set an API key
- Look up as many cities as you like in one session; press Enter on a blank line to quit
- Clear messages for an unknown city, a rejected API key, or no internet connection
- Any API key is read from a `.env` file, so it is never hardcoded or committed

## Quick start

Requires Python 3.

```bash
git clone https://github.com/Saarthi09/Weather-Dashboard.git
cd Weather-Dashboard
pip install -r requirements.txt
python weather.py
```

### Optional: use OpenWeatherMap

1. Get a free key at [openweathermap.org](https://home.openweathermap.org/users/sign_up).
2. Run `cp .env.example .env` and put your key in `.env`.
3. Run `python weather.py`. It prints `Using OpenWeatherMap.`

`.env` is listed in `.gitignore`, so your key stays on your machine.

## How it works

- **Open-Meteo:** the city name goes to Open-Meteo's geocoding API to get latitude and longitude, then a forecast request returns the current conditions and today's min/max. Open-Meteo reports weather as a numeric WMO code, which the app translates into text ("light rain", "overcast", and so on).
- **OpenWeatherMap:** one request to the current-weather endpoint with `units=metric`.
- Both sources return the same fields, so the printing code doesn't care which one answered.
- HTTP requests and JSON parsing use only the standard library (`urllib`, `json`). `python-dotenv` loads the optional key.

## Project structure

```
.
├── weather.py         # The app
├── requirements.txt   # python-dotenv
├── .env.example       # Template for an optional OpenWeatherMap key
└── README.md
```

## Credits

Weather data from [Open-Meteo](https://open-meteo.com/) (free for non-commercial use) and [OpenWeatherMap](https://openweathermap.org/). Location search uses Open-Meteo's geocoding API, which is based on [GeoNames](https://www.geonames.org/).

## Ideas for next steps

- 5-day forecast
- Choose metric or imperial units
- A small GUI or web dashboard on top of the same functions
