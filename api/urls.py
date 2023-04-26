from django.urls import path
from .views import WeatherMailView, send_weather_mail_info

urlpatterns = [
    path('send-weather-mail/', WeatherMailView.as_view(), name='send_weather_mail'),
    path('send_mail/', send_weather_mail_info, name='sendmail')
]