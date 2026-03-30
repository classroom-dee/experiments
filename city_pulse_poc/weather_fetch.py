from __future__ import annotations
import json
from pathlib import Path
from typing import List

import requests


# for dot operator enabling
class DotDict(dict):
    def __getattr__(self, key):
        val = self[key]
        if isinstance(val, dict):
            return DotDict(val)
        if isinstance(val, list):
            return [DotDict(v) if isinstance(v, dict) else v for v in val]
        return val


# Central Park
LAT = 40.769804
LON = -73.974817
WEATHER_URL = f"https://api.weather.gov/points/{LAT},{LON}"

HEADERS = {"User-Agent": "CityPulsePoC/0.1 (Ad Hoc)"}

weather_res = requests.get(WEATHER_URL, headers=HEADERS)
weather_res.raise_for_status()
weather = DotDict(weather_res.json())

sunrise = weather.properties.astronomicalData.sunrise
sunset = weather.properties.astronomicalData.sunset
city = weather.properties.relativeLocation.properties.city
state = weather.properties.relativeLocation.properties.state
tz = weather.properties.timeZone
forecast_url = weather.properties.forecast

forecast_res = requests.get(forecast_url, headers=HEADERS)
forecast_res.raise_for_status()
forecast = DotDict(forecast_res.json())

updated_at = forecast.properties.updateTime
periods: List = forecast.properties.periods

cleaned = {
    "city": city,
    "state": state,
    "timezone": tz,
    "sunrise": sunrise,
    "sunset": sunset,
    "updated_at": updated_at,
    "forecast": periods,
}

curr_dir = Path(__file__).parent
with open(curr_dir / "example.json", "w") as f:
    json.dump(cleaned, f)
