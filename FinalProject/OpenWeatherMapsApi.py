import requests

class WeatherMapsApi:
    def __init__(self, city):
        self.city = city
        self.api_key = '1458a59f23071ab5a48e06c49d6d8a0a'

    def weather_url_word(self):
        return 'https://api.openweathermap.org/data/2.5/weather?q='+self.city +',us&appid='+ self.api_key

    def weather_url_zipCode(self):
        return 'https://api.openweathermap.org/data/2.5/weather?zip='+self.city +',us&appid='+ self.api_key


    def JsonData(self, url):
        return requests.get(url).json()



