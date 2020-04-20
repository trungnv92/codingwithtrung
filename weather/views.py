from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests
# Create your views here.
def list_weather(request):
    context = {
        'status': 'ok',
    }
    return render(request, 'weather/app.html', context)

def index(request): 
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=271d1234d3f497eed5b1d80a07b3fcd1&lang=vi'
    #city = 'Ho Chi Minh'
    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    else:
        form = CityForm()
    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r["main"]["temp"],
            'description': r["weather"][0]["description"],
            'icon': r["weather"][0]["icon"],
        }
        weather_data.append(city_weather)
        print(city_weather)
    context = {'weather_data' : weather_data}
    context['form'] = form
    return render(request, "weather/app.html", context) 

def get_list_data_weather():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=271d1234d3f497eed5b1d80a07b3fcd1&lang=vi'
    #city = 'Ho Chi Minh'
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r["main"]["temp"],
            'description': r["weather"][0]["description"],
            'icon': r["weather"][0]["icon"],
        }
        weather_data.append(city_weather)
        print(city_weather)
    #context = {'weather_data' : weather_data}
    return weather_data