from enum import Enum


class ForecastTypes(Enum):
    """
    Forecast types
    """

    TEMPERATURE = "temperature_2m"
    SHOWER = "showers"
    CLOUD_COVER = "cloudcover"


class Coordinates(Enum):
    """
    Coordinates names
    """

    LATITUDE = "lat"
    LONGITUDE = "lon"
