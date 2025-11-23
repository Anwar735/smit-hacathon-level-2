import os
import requests
from typing import Dict, Any
from urllib.parse import urlencode


OPENWEATHER_KEY = '09681746c1a8146f365cd068ef4afb47'

BASE_WEATHER_URL = 'https://api.openweathermap.org/data/2.5'


class WeatherAPIError(Exception):
    pass


def _do_request(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENWEATHER_KEY:
        raise WeatherAPIError('OpenWeather API key not set')
    params = {**params, 'appid': OPENWEATHER_KEY}
    url = f"{BASE_WEATHER_URL}/{path}?{urlencode(params)}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise WeatherAPIError(f'API request failed: {exc}') from exc
    return resp.json()


def get_current_weather_by_city(city: str) -> Dict[str, Any]:
    return _do_request('weather', {'q': city})


def get_forecast_5day_by_city(city: str) -> Dict[str, Any]:
    return _do_request('forecast', {'q': city})
