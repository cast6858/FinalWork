from datetime import date
from OpenWeatherMapsApi import WeatherMapsApi
from WeatherMapsController import WeatherMapsControl
from TemptureConversion import ConvertTemperature
from CityValidation import ValidationOfCity
from VerifyState import ValidatingState
from flask import Flask , render_template ,request,jsonify, redirect, url_for,flash


app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'BASE_REPLAY'
weather_data = []



def date_time_today():
    today = date.today()
    reformattedDate = today.strftime("%B-%d-%Y")
    return reformattedDate


def temperature_type_scale(temperatureType,temperature_scale,weather_session ):
    regularTemperature = ''
    maxTemp = ''
    minTemp = ''
    symbol = ''
    if(len(temperatureType) != 0):  # Checking to make sure the list is not empty
        if(temperatureType[0] == 'F'):
            regularTemperature = temperature_scale.kelvinToFahrenheit(weather_session.weatherTempature)
            maxTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMax)
            minTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMin)
            symbol = '°F'
        elif(temperatureType[0] == 'C'):
            regularTemperature = temperature_scale.kelvinToCelsius(weather_session.weatherTempature)
            maxTemp = temperature_scale.kelvinToCelsius(weather_session.weatherTemMax)
            minTemp = temperature_scale.kelvinToCelsius(weather_session.weatherTemMin)
            symbol = '°C'
        elif(temperatureType[0] == 'K'):
            regularTemperature = weather_session.weatherTempature
            maxTemp = weather_session.weatherTemMax
            minTemp = weather_session.weatherTemMin
            symbol = '°K'
        else: # If user doesnt choose a type Default is Fahrenherit
            regularTemperature = temperature_scale.kelvinToFahrenheit(weather_session.weatherTempature)
            maxTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMax)
            minTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMin)
            symbol = '°F'
    else: #when the program runs if prevoius data exists it poplates old data until new data is present bt default always Fahrenheit
        regularTemperature = temperature_scale.kelvinToFahrenheit(weather_session.weatherTempature)
        maxTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMax)
        minTemp = temperature_scale.kelvinToFahrenheit(weather_session.weatherTemMin)
        symbol = '°F'

    return  regularTemperature,maxTemp,minTemp,symbol


def conntect_api_weather(city):
    weatherRequest = WeatherMapsApi(city)
    url = weatherRequest.WeatherUrl()
    json_object = weatherRequest.JsonData(url)
    return json_object


def city_validation(json_object):
    try:
        cityFlag = ValidationOfCity(json_object)
        status = cityFlag.status_code()
        return status
    except:
        print("Couldnt validate city!")


def weather_call(city):
    flag_city = ''
    try:
        json_object = conntect_api_weather(city)
        cityFlag = city_validation(json_object) # making sure user inserts a correct city
        if(cityFlag == False):
            flag_city = False
        else:
            flag_city = True
    except:
        print("Failed To Find Data information")
    return flag_city




@app.errorhandler(500)
def server_issue(expecption):
    print(expecption)

    return render_template("500.html")

@app.errorhandler(404)
def server_issue(expecption):
    print(expecption)

    return render_template("404.html")



@app.route("/", methods=['GET','POST'])
def index():
    city = ''
    weather = ''
    error = True
    abbrevation = ''
    temperatureType = ''
    todaysDate = date_time_today()
    if request.method == 'POST':
        city = request.form.get('city_Lookup')
        abbrevation = request.form.get('state_Lookup')
        temperatureType = request.form.getlist('option')
    weather = weather_call(city)
    if not weather: #validated cVaity
        json_object = conntect_api_weather(city)
        weather_session = WeatherMapsControl(json_object)

        if weather_session.weatherName != None:
            verfied_state = ValidatingState()
            print(verfied_state.state_look_up(weather_session.weatherName))

            temperature_scale = ConvertTemperature()

            temperatures_scale_Returned = temperature_type_scale(temperatureType,temperature_scale,weather_session)
            normalTemp = str(temperatures_scale_Returned).split(",")[0].replace("(","").strip()
            maxTemp = str(temperatures_scale_Returned).split(",")[1].replace("(", "").strip()
            minTemp = str(temperatures_scale_Returned).split(",")[2].replace("(", "").strip()
            symbol = str(temperatures_scale_Returned).split(",")[3].replace(")", "").strip()

            weatherInfo = {
                'city': weather_session.weatherName,
                'temperature': normalTemp+ " "+ symbol,
                'temperature_max': maxTemp+ " "+ symbol,
                'temperature_min': minTemp+" "+ symbol,
                'pressure': str(weather_session.weatherPressure)+" hPa",
                'humidity': str(weather_session.weatherHumidity)+ "%",
                'icon': weather_session.weatherIcon
            }
            error = False
            weather_data.append(weatherInfo)

    else:
        error = True
        weatherInfo = {
            'city': "",
            'temperature': "",
            'temperature max': "",
            'temperature min': "",
            'pressure': "",
            'humidity': "",
             'icon': ""}
        error_message = 'Error message'
    if error and temperatureType != "":
        errorTpye = ''
        if city.isnumeric():
            errorTpye = 'zip code'
        else:
            errorTpye = 'city'
        flash("Please insert a correct "+ errorTpye + " this is invalid. Please retype or check spelling", 'error')



    return render_template("index.html",weatherInfo=weatherInfo , todaysDate = todaysDate)


if __name__ == '__main__':
    app.run()
