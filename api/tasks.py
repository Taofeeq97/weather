# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from .serializers import WeatherRealtimeSerializer
import requests


@shared_task
def send_weather_mail():
    weather_url = "https://weatherapi-com.p.rapidapi.com/current.json"

    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "7613a5777dmshc0a19d85c6372d7p197f98jsn2c004a89fa6d",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    locations = ['london', 'canada', 'lagos']

    weather_data = []

    for location in locations:
        url_query = {'q': location}
        response = requests.get(url=weather_url, params=url_query, headers=headers)
        serializer = WeatherRealtimeSerializer(response.json())
        weather_data.append(serializer.data)

    message = ""
    for data in weather_data:
        location = data['name']
        temperature = data['temp_c']
        condition = data['condition']['text']
        message += f" Today's temperature in {location} is {temperature}°C and it is going to be {condition}\n"

    send_mail(
        'Weather Update',
        message,
        'taomi1997@gmail.com',
        ['otutaofeeqi@gmail.com'],
        fail_silently=False,
    )
