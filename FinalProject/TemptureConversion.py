
class ConvertTemperature():

    def kelvinToFahrenheit(self, temperture):
        kelvinConvertedFH = 9 / 5 * (temperture - 273) + 32
        formattedFH = round(kelvinConvertedFH, 0)
        return formattedFH

    def kelvinToCelsius(self, temperture):
        kelvinConvertedCl = temperture = 271.15
        formattedCl = round(kelvinConvertedCl, 0)
        return formattedCl
