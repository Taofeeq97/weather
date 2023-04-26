from rest_framework import serializers


class WeatherRealtimeSerializer(serializers.Serializer):
    name = serializers.CharField(source='location.name')
    region = serializers.CharField(source='location.region')
    country = serializers.CharField(source='location.country')
    localtime = serializers.DateTimeField(source='location.localtime')
    temp_c = serializers.FloatField(source='current.temp_c')
    is_day = serializers.IntegerField(source='current.is_day')
    condition = serializers.DictField(source='current.condition')
