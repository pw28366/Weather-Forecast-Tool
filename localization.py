"""To handle fetching city coordinates"""
import logging
import json
import sys
from api_requests import ApiRequests


class CityLocalization:
    """Gather coordinates based on city name and street"""

    def __init__(self, city: str, street: str):
        self.city = city
        self.street = street

    def _build_coordinates_request_url(self) -> str:
        """Build URL for coordinates API call

        Returns:
            str: URL for API call
        """
        return f"https://geocode.maps.co/search?city={self.city}&street={self.street}"

    def get_coordinates_from_response(self) -> dict:
        """Get coordinates from API response

        Returns:
            dict: Dictionary {"lat": value, "lon": value} or closing app if response is wrong
        """
        url = self._build_coordinates_request_url()
        coordinates_request_response = ApiRequests.api_get_request(url)
        if self._check_response_content(coordinates_request_response):
            return {
                "lat": round(float(coordinates_request_response[0]["lat"]), 2),
                "lon": round(float(coordinates_request_response[0]["lon"]), 2),
            }
        else:
            logging.info("Localization did not find - please Check City and Street")
            sys.exit()

    def _check_response_content(self, response: json) -> bool:
        """Validation if the Api resoponse is not empty

        Args:
            response (json): API response in JSON format

        Returns:
            bool: True if JSON is not empty, else False
        """

        if len(response) > 0:
            return True
        return False
