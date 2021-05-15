
class WeatherMapsControl:
    def __init__(self, json_payload):
        self.weatherName = json_payload["name"]
        self.json_payload = json_payload
        self.weatherMain = json_payload['weather'][0]['main'] #Type like clouds
        self.weatherDesciption = json_payload['weather'][0]['description'] #Description data
        self.weatherPressure = json_payload['main']['pressure']
        self.weatherTempature = json_payload['main']['temp'] #Normal Tempurture
        self.weatherFeelsLike = json_payload['main']['feels_like']
        self.weatherTemMin = json_payload['main']['temp_min'] #Min Tempurture
        self.weatherTemMax = json_payload['main']['temp_max'] #Max Tempurture
        self.weatherHumidity = json_payload['main']['humidity'] #Humidity
        self.weatherIcon = json_payload['weather'][0]['icon']
        self.weatherClouds = json_payload['clouds']['all']



    def __str__(self):
        return(self.weatherMain ,self.weatherHumidity)
