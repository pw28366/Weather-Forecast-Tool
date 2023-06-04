"""To handle fetching different types of wheater
"""
import json
from api_requests import ApiRequests


class CityForecast:
    """Class for checking forecast for particular coordinates, number of days and type"""

    def __init__(self, coordinates: dict, days: str, forecast_type: str):
        self.longitude = coordinates["lon"]
        self.latitude = coordinates["lat"]
        self.days = days
        self.forecast_type = forecast_type

    def _build_forecast_request_url(self) -> str:
        """API call url format

        Returns:
            str: URL in format ready to use in API call
        """
        return f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly={self.forecast_type}&forecast_days={self.days}"

    def make_forecast_request(self) -> json:
        """Api call with proper URL

        Returns:
            json: Request result in JSON format
        """
        url = self._build_forecast_request_url()
        return ApiRequests.api_get_request(url)


class DetailedForecast(CityForecast):
    """Class for checking detailes forecast for trip planning - for particular date and following features:
    weathercode,temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,windspeed
    """

    def __init__(self, coordinates: dict, start_date: str, end_date: str):
        self.longitude = coordinates["lon"]
        self.latitude = coordinates["lat"]
        self.start_date = start_date
        self.end_date = end_date

    def _build_forecast_request_url(self) -> str:
        """API call url format

        Returns:
            str: URL in format ready to use in API call
        """
        return f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,windspeed_10m_max&start_date={self.start_date}&end_date={self.end_date}&timezone=Europe%2FBerlin"


class HistoricalWeather(DetailedForecast):
    """Class for checking historical temperature forecast"""

    def __init__(self, coordinates: dict, start_date: str, end_date: str):
        self.longitude = coordinates["lon"]
        self.latitude = coordinates["lat"]
        self.start_date = start_date
        self.end_date = end_date

    def _build_forecast_request_url(self) -> str:
        """API call url format

        Returns:
            str: URL in format ready to use in API call
        """
        return f"https://archive-api.open-meteo.com/v1/archive?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=temperature_2m"
