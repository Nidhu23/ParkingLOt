from django.urls import path
from Users import views

urlpatterns = [
    path('register/', views.register),
]
