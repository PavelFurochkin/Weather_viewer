import requests

from django.conf import settings

from weather_app.dto import LocationWeatherDTO
from .mapper import LocationWeatherMapper


class WeatherApiService:
    __SECRET_KEY = settings.WEATHER_API_KEY

    @classmethod
    def get_locations_by_name(cls, name: str, limit: int = 5, ) -> list[LocationWeatherDTO]:
        __url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {'q': name,
                  'limit': limit,
                  'appid': cls.__SECRET_KEY,
                  'land': 'ru'}
        try:
            response = requests.get(__url, params)
            response.raise_for_status()
            data = response.json()
            return [
                LocationWeatherDTO(
                    name=loc.get('name'),
                    country=loc.get('country'),
                    longitude=loc.get('longitude'),
                    latitude=loc.get('latitude')
                )
                for loc in data
            ]
        except requests.HTTPError as e:
            print(f'Ошибка: {e}')

    @classmethod
    def get_location_by_coord(cls, lat: float, lon: float) -> LocationWeatherDTO:
        __url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'lat': lat,
                  'lon': lon,
                  'appid': cls.__SECRET_KEY,
                  'land': 'ru',
                  'units': 'metric'}
        try:
            response = requests.get(__url, params)
            response.raise_for_status()
            data = response.json()
            return LocationWeatherMapper.dict_to_dto(data)
        except requests.HTTPError as e:
            print(f'Ошибка: {e}')



