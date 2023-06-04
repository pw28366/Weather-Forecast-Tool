""" Main module"""
import datetime
import logging
import sys
import folium
import matplotlib.pyplot as plt
import pandas as pd

from PyQt6.QtWidgets import QApplication
from app_menu import CliMenu
from localization import CityLocalization
from forecast import CityForecast, HistoricalWeather, DetailedForecast
from logging_settings import set_logger
from enums import ForecastTypes, Coordinates
from ux import MainWindow


def app_run():
    """Run console application and print menu"""
    CliMenu.print_start_menu()
    user_option = CliMenu.choose_option()

    if user_option == 1:
        run_option_1()
        app_run()

    elif user_option == 2:
        run_option_2()
        app_run()

    elif user_option == 3:
        run_option_3()
        app_run()

    elif user_option == 4:
        run_option_4()
    else:
        print("Error: Invalid option. please enter a number between 1 and 4.")
        app_run()


def build_one_data_frame(days: str, coords_dict: dict, data: ForecastTypes):
    """Function to build one dataframe from API response as JSON

    Args:
        days (str): Number of forecast days
        coords_dict (dict): Coordinates of the city
        data (ForecastTypes): Type of forecasts - Enum type

    Returns:
        dataframe: Pandas DataFrame
    """
    city_forecast_data = CityForecast(coords_dict, days, data.value)
    forecast_request_response = city_forecast_data.make_forecast_request()
    time_hourly = forecast_request_response["hourly"]["time"]
    data_value = forecast_request_response["hourly"][data.value]

    # Build dataframe from lists
    data_f = pd.DataFrame(data_value, index=time_hourly, columns=[data.value])
    return data_f


def build_data_frames(days: str, coords_dict: dict) -> list:
    """Build all data frames for option 1
    Args:
        days (str): Number of forecast days
        coords_dict (dict): Coordinates of the city

    Returns:
        list: list of dataframes
    """
    dataframe = []

    for data in ForecastTypes:
        data_f = build_one_data_frame(days, coords_dict, data)
        dataframe.append(data_f)
    return dataframe


def set_plot_paramerers(city: str, days: str):
    """Set parameters for plot

    Args:
        city (str): City name
        days (str): Number of days
    """
    plt.xticks(rotation=45)
    plt.ylabel("Data")
    plt.xlabel("Time")
    plt.locator_params(nbins=10)
    plt.title(f"{days} days Forecast for {city}")
    plt.legend()


def run_option_1():
    """OPTION 1: Check weather forecast for particular localization \
        - temperature, shower, cloudcover"""
    city = (
        input("Enter city or press Enter to use default value [Wroclaw]: ") or "Wroclaw"
    )
    street = (
        input("Enter street or press Enter to use default value [Fabryczna]: ")
        or "Fabryczna"
    )
    days = (
        input("Enter number of days (max 16) or press Enter to use default value [5]: ")
        or "5"
    )
    if not 0 < int(days) < 17:
        logging.info("Error: You can choose only from 1 to 15 days \n")
        sys.exit()
    logging.info("INFO: Api call for city coordinates \n")
    city_loc = CityLocalization(city, street)
    coords_dict = city_loc.get_coordinates_from_response()
    logging.info(
        "INFO: %s days forecast will be prepared for city: %s and street: %s - coordinates: %s : %s \n",
        days,
        city,
        street,
        coords_dict[Coordinates.LATITUDE.value],
        coords_dict[Coordinates.LONGITUDE.value],
    )
    if not CliMenu.check_if_key_pressed():
        sys.exit()

    data_frame_list = build_data_frames(days, coords_dict)
    ax = data_frame_list[0].plot()
    data_frame_list[1].plot(ax=ax)
    data_frame_list[2].plot(ax=ax)
    logging.info("INFO: Please check opened plot in separate window")
    set_plot_paramerers(city, days)
    plt.show()


def prepare_dates_range(
    start_date: datetime, forecast_days: int, history_years: int
) -> dict:
    """Function to calculate date ranges based on start date, numer of forecast days and number of years for historical data

    Args:
        start_date (datetime): Start date in format YYYY-MM-DD
        forecast_days (int): Number of days
        history_years (int): Number of years

    Returns:
        dict: Dict with date ranges {"YYY-MM-DD":"YYYY-MM-DD"}
    """
    SHIFT_TIME = "%Y-%m-%d"
    dates_ranges = {}
    start_day = start_date.day
    start_year = start_date.year - 1
    start_month = start_date.month
    end_day = start_day + int(forecast_days) - 1

    for _ in range(history_years):
        today_date = datetime.datetime(start_year, start_month, start_day).date()
        end_date = datetime.datetime(start_year, start_month, end_day).date()
        dates_ranges[today_date.strftime(SHIFT_TIME)] = end_date.strftime(SHIFT_TIME)
        start_year -= 1
    return dates_ranges


def build_data_frames_historical(coords_dict: dict, dates: dict) -> list:
    """Build Dataframes for particular date ranges

    Args:
        coords_dict (dict): City coordinates
        dates (dict): Date ranges

    Returns:
        list: List of dataframes
    """
    dataframe = []
    for key, value in dates.items():
        city_historical_data = HistoricalWeather(coords_dict, key, value)
        forecast_request_response = city_historical_data.make_forecast_request()
        time_hourly = forecast_request_response["hourly"]["time"]
        data_value = forecast_request_response["hourly"]["temperature_2m"]
        data_f = pd.DataFrame(data_value, index=time_hourly, columns=[key[:4]])
        dataframe.append(data_f)
    return dataframe


def run_option_2():
    """OPTION 2: Check weather temperature forecast for particular localization and days and add historical data from number of years"""
    city = (
        input("Enter city or press Enter to use default value [Wroclaw]: ") or "Wroclaw"
    )
    street = (
        input("Enter street or press Enter to use default value [Fabryczna]: ")
        or "Fabryczna"
    )
    forecast_days = (
        input(
            "Enter numbers of days (max 16) or press Enter to use default value [5]: "
        )
        or "5"
    )
    historical_data = (
        input(
            "Enter numbers of years (history) or press Enter to use default value [4]: "
        )
        or "4"
    )
    if not 0 < int(forecast_days) < 17:
        logging.info("Error: You can choose only from 1 to 15 days \n")
        sys.exit()
    city_loc = CityLocalization(city, street)
    coords_dict = city_loc.get_coordinates_from_response()
    logging.info(
        "%s days forecast (compared with last %s years) will be prepared for city: %s and street: %s - coordinates: %s : %s \n",
        forecast_days,
        historical_data,
        city,
        street,
        coords_dict[Coordinates.LATITUDE.value],
        coords_dict[Coordinates.LONGITUDE.value],
    )

    if not CliMenu.check_if_key_pressed():
        sys.exit()
    dates = prepare_dates_range(
        datetime.datetime.now().date(), forecast_days, int(historical_data)
    )
    data_frame_list = build_data_frames_historical(coords_dict, dates)
    ax = data_frame_list[0].plot()
    for data_frame in data_frame_list[1:]:
        data_frame.plot(ax=ax)
    forcast_data_frame = build_one_data_frame(
        forecast_days, coords_dict, ForecastTypes.TEMPERATURE
    )
    forcast_data_frame.plot(ax=ax)

    set_plot_paramerers(city, str(forecast_days))
    plt.show()
    print()


def run_option_3():
    """OPTION 3: Read trip details from CSV file, check wheater forecasts for all places and show them on map"""
    # read trip details from CSV file
    try:
        csv_file = pd.read_csv("route_data.csv")
    except FileNotFoundError:
        logging.info("File not found.")
    except pd.errors.EmptyDataError:
        logging.info("No data")
    except pd.errors.ParserError:
        logging.info("Parse error")
    except Exception:
        logging.info("Some other exception")
    # displaying the contents of the CSV file
    lat = []
    lon = []
    weathercode = []
    temperature_max = []
    temperature_min = []
    rain_sum = []
    shower_sum = []
    wind_speed = []

    # Get forecast information for trip places
    for index, row in csv_file.iterrows():
        # Get city coodinations
        city_loc = CityLocalization(row["City"], row["Street"])
        coords_dict = city_loc.get_coordinates_from_response()
        lat.append(coords_dict["lat"])
        lon.append(coords_dict["lon"])
        # Get forecast
        fetched_forecast = DetailedForecast(coords_dict, row["Date"], row["Date"])
        json_with_data = fetched_forecast.make_forecast_request()
        # Fetch data from JSON and append to lists
        weathercode.append(json_with_data["daily"]["weathercode"])
        temperature_max.append(json_with_data["daily"]["temperature_2m_max"])
        temperature_min.append(json_with_data["daily"]["temperature_2m_min"])
        rain_sum.append(json_with_data["daily"]["rain_sum"])
        shower_sum.append(json_with_data["daily"]["showers_sum"])
        wind_speed.append(json_with_data["daily"]["windspeed_10m_max"])

    # Add lists to dataframes as columns
    csv_file["Latitude"] = lat
    csv_file["Longitude"] = lon
    csv_file["Wheatercode"] = weathercode
    csv_file["Temp_max"] = temperature_max
    csv_file["Temp_min"] = temperature_min
    csv_file["Rain_sum"] = rain_sum
    csv_file["Shower_sum"] = shower_sum
    csv_file["Wind_speed_max"] = wind_speed

    logging.info("Current dataframe shape: \n")
    logging.info(csv_file)

    # Find center localization to set map center position
    lat_center = lambda lat: (lat[0] + lat[-1]) / 2
    lon_center = lambda lon: (lon[0] + lon[-1]) / 2

    # Create Folum map
    folium_map = folium.Map(location=[lat_center(lat), lon_center(lon)], zoom_start=7)
    # Iterate over dataframe and generate markers on map - check if value of rain or shower is grater than 0 and set marker color as "RED"
    for index, row in csv_file.iterrows():
        if row["Rain_sum"][0] > 0 or row["Shower_sum"][0] > 0:
            color = "red"
        else:
            color = "blue"
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            radius=10,
            popup=(
                "City: " + str(row["City"]) + "<br>"
                "Date: " + str(row["Date"]) + "<br>"
                "Wheatercode: " + str(row["Wheatercode"]) + "<br>"
                "Temp_max: " + str(row["Temp_max"]) + "<br>"
                "Temp_min: " + str(row["Temp_min"]) + "<br>"
                "Rain_sum: " + str(row["Rain_sum"]) + "<br>"
                "Shower_sum: " + str(row["Shower_sum"]) + "<br>"
                "Wind_speed_max:" + str(row["Wind_speed_max"]) + "<br>"
            ),
            icon=folium.Icon(icon=str(index + 1), prefix="fa", color=color),
        ).add_to(folium_map)
    folium_map.save("map.html")

    # Run pyQT app and show saved map as interactive HTML map
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


def run_option_4():
    """OPTION 4: To close the app"""
    logging.info("You pressed option 4 to close app..")
    logging.info("Closing app...")
    sys.exit()


if __name__ == "__main__":
    set_logger()
    app_run()
