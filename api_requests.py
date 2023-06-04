"""To hangle api calls

"""
import json
import logging
import requests
import urllib3


class ApiRequests:
    """Class for API calls service

    Raises:
        SystemExit: Wrong api request / response

    Returns:
        json: response in json format
    """

    @staticmethod
    def api_get_request(url: str) -> json:
        """_summary_

        Args:
            url (str): Url for api call

        Raises:
            SystemExit: Could not decode the text into json, Error: A Connection error occurred.

        Returns:
            json: api response in json format
        """
        try:
            urllib3.disable_warnings()
            api_request = requests.get(url=url, verify=False, timeout=10)
            return api_request.json()
        except requests.exceptions.TooManyRedirects:
            logging.info("Error: Too many redirects.")
            return False
        except requests.exceptions.JSONDecodeError:
            logging.info("Error: Could not decode the text into json")
            return False
        except requests.exceptions.ConnectionError:
            logging.info("Error: A Connection error occurred.")
            return False
        except requests.exceptions.InvalidURL:
            logging.info("Error: The URL provided was somehow invalid.")
            return False
        except requests.exceptions.RequestException as error:
            logging.info("Fatal error: App will be closed")
            raise SystemExit(error) from error
