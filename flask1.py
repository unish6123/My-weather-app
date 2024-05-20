from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather_data(city)
        return render_template('index.html', weather_data=weather_data)
    return render_template('index.html', weather_data=None)

def get_weather_data(city):
    api_key = "7edbea9f9c59457e98a225317241505"
    url1 = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    url2 = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}"
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()
        weather_data = {
            'time': getTime(data1),
            'temp_c': getTempC(data1),
            'temp_f': getTempF(data1),
            'feels_like_c': feelsLikeC(data2),
            'feels_like_f': feelsLikeF(data2),
            'max_temp_c': maxTempC(data2),
            'max_temp_f': maxTempF(data2),
            'is_sunny': isItSunnyOrNot(data2),
            'condition': conditionOutside(data2),
            'city': city
        }
        return weather_data
    else:
        return print('This is not a valid address.')

def getTime(data):
    dateTime = data['location']['localtime']
    return dateTime.split(' ')[1]

def getTempC(data):
    return data['current']['temp_c'] 

def getTempF(data):
    return data['current']['temp_f']

def isItSunnyOrNot(data2):
    weigher = data2['forecast']['forecastday'][0]['day']['daily_will_it_rain']
    if weigher == 0:
        return "won't"
    else:
        return "will"

def feelsLikeC(data2):
    return data2['current']['feelslike_c']

def feelsLikeF(data2):
    return data2['current']['feelslike_f']

def maxTempC(data2):
    return data2['forecast']['forecastday'][0]['day']['maxtemp_c']

def maxTempF(data2):
    return data2['forecast']['forecastday'][0]['day']['maxtemp_f']

def conditionOutside(data2):
    return data2['forecast']['forecastday'][0]['day']['condition']['text']


def notAvalidAddress():
    return None

if __name__ == "__main__":
    app.run(debug=True)
