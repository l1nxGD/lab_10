import requests
from json import loads

class Api:

      def __init__(self, cityName):
            self.cityName = cityName
            self.apiKey = "5c0e6a096ab232d92dc3890fe8a59a3e"

      def getData(self):
            r = requests.post(f"https://api.openweathermap.org/data/2.5/weather?q={self.cityName}&appid={self.apiKey}")
            data = loads(r.text)

            return data
'''
            print(f"Сейчас в {self.cityName}:\n"
                  f"Температура: {round(data['main']['temp'] - 273.15, 2)} c\n"
                  f"Погода: {data['weather'][0]['main']}\n"
                  f"Влажность: {data['main']['humidity']}%\n"
                  f"Давление: {data['main']['pressure']} Pa\n")
'''
