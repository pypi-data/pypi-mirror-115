# Taranis

[![Version](https://img.shields.io/pypi/v/taranis)](https://pypi.org/project/taranis/)
[![Build](https://img.shields.io/github/workflow/status/esadek/taranis/CI)](https://github.com/esadek/taranis/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/esadek/taranis)](https://github.com/esadek/taranis/blob/main/LICENSE)

Taranis is a Python API wrapper for [weather-api](https://github.com/robertoduessmann/weather-api). It provides quick and easy retrieval of weather data for a given city.

## Installation:

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):

```
pip install -U taranis
```

## Usage:

Import the module:

```python
>>> import taranis
```

Then call any of the below functions:

```python
>>> taranis.get_weather('San Francisco')
{'temperature': '+15 °C', 'wind': '24 km/h', 'description': 'Partly cloudy', 'forecast': [{'day': '1', 'temperature': '20 °C', 'wind': '18 km/h'}, {'day': '2', 'temperature': '16 °C', 'wind': '22 km/h'}, {'day': '3', 'temperature': '17 °C', 'wind': '12 km/h'}]}
```

```python
>>> taranis.get_temperature('San Francisco')
'+15 °C'
```

```python
>>> taranis.get_wind('San Francisco')
'24 km/h'
```

```python
>>> taranis.get_description('San Francisco')
'Partly cloudy'
```

```python
>>> taranis.get_forecast('San Francisco')
[{'day': '1', 'temperature': '20 °C', 'wind': '18 km/h'}, {'day': '2', 'temperature': '16 °C', 'wind': '22 km/h'}, {'day': '3', 'temperature': '17 °C', 'wind': '12 km/h'}]
```