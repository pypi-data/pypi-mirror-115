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
    str
        Current temperature for given city.
    """
    return get_weather(city)["temperature"]


def get_wind(city: str) -> str:
    """Return current wind speed for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    str
        Current wind speed for given city.
    """
    return get_weather(city)["wind"]


def get_description(city: str) -> str:
    """Return description of current weather for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    str
        Description of current weather for given city.
    """
    return get_weather(city)["description"]


def get_forecast(city: str) -> list:
    """Return a list of dictionaries containing forecast data for given city.

    Parameters
    ----------
    city : str
        Name of city.

    Returns
    -------
    list
        List of dictionaries containing forecast data for given city.
    """
    return get_weather(city)["forecast"]
