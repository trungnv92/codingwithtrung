from django.urls import path
from .views import list_weather, index
app_name = 'weather'
urlpatterns = [
    path('app/', index, name='list_weather'),
    path('', index, name="index")
]
