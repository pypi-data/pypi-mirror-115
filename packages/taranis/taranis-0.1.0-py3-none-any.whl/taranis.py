from requests import get


def get_weather(city: str) -> dict:
    """Return a dictionary containing weather data for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    weather : dict
        Dictionary containing weather data for given city.
    """
    if type(city) != str:
        raise TypeError("city must be a string")
    url = "https://goweather.herokuapp.com/weather/"
    weather = get(url + city.replace(" ", "")).json()
    if weather == {"message": "NOT_FOUND"}:
        raise ValueError("weather not found")
    return weather


def get_temperature(city: str) -> str:
    """Return current temperature for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    temperature : str
        Current temperature for given city.
    """
    temperature = get_weather(city)["temperature"]
    return temperature


def get_wind(city: str) -> str:
    """Return current wind speed for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    wind : str
        Current wind speed for given city.
    """
    wind = get_weather(city)["wind"]
    return wind


def get_description(city: str) -> str:
    """Return description of current weather for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    description : str
        Description of current weather for given city.
    """
    description = get_weather(city)["description"]
    return description


def get_forecast(city: str) -> list:
    """Return a list of dictionaries containing forecast data for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    forecast : list
        List of dictionaries containing forecast data for given city.
    """
    forecast = get_weather(city)["forecast"]
    return forecast
