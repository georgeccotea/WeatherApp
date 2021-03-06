import json
import sys
from configparser import ConfigParser
from urllib import parse, request

STOCK_URL = "http://api.openweathermap.org/data/2.5/weather"

def provideSecrets():
    config = ConfigParser()
    config.read("api.ini")
    return config["openweather"]["api_key"]

def userToComputer():
    return " ".join(sys.argv[1:])

def queryBuilder(city_input):
    api_key = provideSecrets()
    encoded_city_name = parse.quote_plus(city_input)
    units = "metric"
    url = (
        f"{STOCK_URL}?q={encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url

def tickleAPI(query_url):
    response = request.urlopen(query_url)
    data = response.read()
    return json.loads(data)

if __name__ == "__main__":
    location = userToComputer()
    query_url = queryBuilder(location)
    weather_data = tickleAPI(query_url)
    print(
      f"{weather_data['name']} ({weather_data['coord']['lon']}, {weather_data['coord']['lat']}): "
      f"{weather_data['weather'][0]['description']} "
      f"{weather_data['main']['temp']}"
      "°C"
    )
    print(f"Minimum Temperature: {weather_data['main']['temp_min']}°C")
    print(f"Maximum Temperature: {weather_data['main']['temp_max']}°C")
    print(f"Current Pressure: {weather_data['main']['pressure']} hPa")
    print(f"Humidity: {weather_data['main']['humidity']}%")
    print(f"Wind Speed and Angle: {weather_data['wind']['speed']} m/s, {weather_data['wind']['deg']}°")
