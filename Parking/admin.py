from django.contrib import admin
from .models import VehicleType, ParkingType, Parking, UnPark
# Register your models here.
admin.site.register(VehicleType)
admin.site.register(Parking)
admin.site.register(ParkingType)
admin.site.register(UnPark)