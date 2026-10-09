# Weather CLI

A command-line weather app in Python. Type a city, get its current weather from the [OpenWeatherMap API](https://openweathermap.org/current).

```
$ python weather.py
Enter city (blank to quit): Toronto
Retrieving weather for Toronto
City: Toronto, CA
Temperature: 12.3°C (feels like 11.0°C)
Condition: light rain
Wind speed: 4.6 m/s
Max temp: 14.1°C
Min temp: 10.0°C
Enter city (blank to quit): Atlantis
Retrieving weather for Atlantis
City not found, try again.
```

## Features

- Current temperature and "feels like" temperature, in °C
- Weather description, wind speed, and the day's min/max
- Look up as many cities as you like in one session; press Enter on a blank line to quit
- Clear messages for an unknown city, a rejected API key, or no internet connection
- API key loaded from a `.env` file, so it is never hardcoded or committed

## How it works

1. `python-dotenv` loads `OPENWEATHER_API_KEY` from `.env`.
2. The city and key are URL-encoded into a request to the current-weather endpoint, with `units=metric`.
3. The JSON response is parsed with the standard `json` module and the useful fields are printed.

Only the standard library (`urllib`, `json`) is used for the HTTP request and parsing.

## Setup

Requires Python 3 and a free API key from [openweathermap.org](https://home.openweathermap.org/users/sign_up).

```bash
git clone https://github.com/Saarthi09/Weather-Dashboard.git
cd Weather-Dashboard
pip install -r requirements.txt
cp .env.example .env        # then put your key in .env
python weather.py
```

`.env` is listed in `.gitignore`, so your key stays on your machine.

## Project structure

```
.
├── weather.py         # The app
├── requirements.txt   # python-dotenv
├── .env.example       # Template for your API key
└── README.md
```

## Ideas for next steps

- 5-day forecast using the `/forecast` endpoint
- Choose metric or imperial units
- A small GUI or web dashboard on top of the same request code
