from .serializers import WeatherRealtimeSerializer
import requests
from django.core.mail import send_mail
from rest_framework.views import APIView

from django.http import HttpResponse
from django.views import View
from api.tasks import send_weather_mail
from weather.models import Profile,Location


class WeatherSendApiView(View):
    def get(self, request):
        send_weather_mail.delay()
        return HttpResponse('Weather mail scheduled successfully!')


class SendMailApiView(APIView):

    def get(self, request):
        user_email='otutaofeeqi@gmail.com'
        profiles = Profile.objects.filter(email=user_email)
        for profile in profiles:
            location_names = [location.name for location in profile.location.all()]
            weather_url = "https://weatherapi-com.p.rapidapi.com/current.json"

            headers = {
                "content-type": "application/octet-stream",
                "X-RapidAPI-Key": "7613a5777dmshc0a19d85c6372d7p197f98jsn2c004a89fa6d",
                "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
            }

            weather_data = []
            for location in location_names:
                url_query = {'q': location}
                try:
                    response = requests.get(url=weather_url, params=url_query, headers=headers)
                    serializer = WeatherRealtimeSerializer(response.json())
                    weather_data.append(serializer.data)
                except Exception as e:
                    print(f"Error getting weather data for {location}: {str(e)}")

            message = ""
            for data in weather_data:
                location = data['name']
                temperature = data['temp_c']
                condition = data['condition']['text']
                message += f"Today's temperature in {location} is {temperature}°C and it is going to be {condition}\n"

            print(message)

            send_mail(
                'Weather Update',
                message,
                'taomi1997@gmail.com',
                [profile.email],
                fail_silently=False,
            )
        return HttpResponse('Email send')




