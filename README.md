# Weather CLI

A simple command-line weather application built with Python using the OpenWeatherMap API.

It retrieves the current weather for a user-entered city and displays key information such as temperature, weather conditions, wind speed, and daily minimum and maximum temperatures.

## Features

- Search weather by city
- Current temperature and "feels like" temperature
- Weather description
- Wind speed
- Daily minimum and maximum temperatures
- Metric units (°C)

## Tech Stack

- Python
- OpenWeatherMap API
- `urllib`
- `json`
- `python-dotenv`

## Setup

1. Clone the repository.
2. Install the required package:

```bash
pip install python-dotenv
```

3. Create a `.env` file in the project directory:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

4. Run the program:

```bash
python weather.py
```

## Example

```
Enter city: Toronto

City: Toronto, CA
Temperature: 24.8°C (feels like 26.1°C)
Condition: scattered clouds
Wind speed: 4.12
Max temp: 26.0
Min temp: 23.5
```

## Notes

- Requires an API key from OpenWeatherMap.
- Uses the current weather endpoint.
- The `.env` file is intentionally excluded from version control.
