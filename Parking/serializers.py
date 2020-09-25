from rest_framework import serializers
from .models import Parking, UnPark


class ParkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = [
            'vehicle_num', 'vehicle_type', 'park_type', 'user', 'disabled',
            'vehicle_color'
        ]


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['vehicle_num', 'vehicle_color', 'vehicle_type', 'slot']
