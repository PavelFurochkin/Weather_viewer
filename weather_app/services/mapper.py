from weather_app.dto import LocationWeatherDTO


class LocationWeatherMapper:
    @classmethod
    def dict_to_dto(cls, data: dict) -> LocationWeatherDTO:
        return LocationWeatherDTO(
            temperature=round(data.get('main', {}).get('temp', 0.0)),
            temperature_feels_like=round(data.get('main', {}).get('feels_like', 0.0)),
            weather_desc=data.get('weather', [{}])[0].get('description'),
            humidity=round(data.get('main', {}).get('humidity', 0.0)),
            wind_speed=data.get('wind', {}).get('speed', 0.0),
            icon_id=data.get('weather', [{}])[0].get('icon'),
            name=data.get("name"),
            country=data.get('sys', {}).get('country'),
            latitude=data.get('coord', {}).get('lon'),
            longitude=data.get('coord', {}).get('lat')
        )

