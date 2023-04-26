# views.py

from django.http import HttpResponse
from django.views import View
from api.tasks import send_weather_mail
from .serializers import WeatherRealtimeSerializer
import requests
from django.core.mail import send_mail


class WeatherMailView(View):
    def get(self, request):
        send_weather_mail_info.delay()
        return HttpResponse('Weather mail scheduled successfully!')


def send_weather_mail_info(request):
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