from django.urls import path
from Parking import views

urlpatterns = [
    path('park/', views.park),
    path('unpark/', views.unpark),
    path('searchbynum/', views.vehicle_num_search)
]
