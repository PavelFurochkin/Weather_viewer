from dataclasses import dataclass


@dataclass
class LocationWeatherDTO:
    temperature: int = None
    temperature_feels_like: int = None
    weather_desc: str = None
    humidity: float = None
    wind_speed: float = None
    icon_id: str = None
    name: str = None
    country: str = None
    latitude: float = None
    longitude: float = None

