from django.urls import path
from .views import SendMailApiView,WeatherSendApiView

urlpatterns = [
    path('send/',WeatherSendApiView.as_view(), name='weather'),
    path('send_mail/', SendMailApiView.as_view(), name='sendmail')
]