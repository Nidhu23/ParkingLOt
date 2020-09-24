import json
from .models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "arav",
            "password": "password1234",
            "role": "security",
            "email": "vivek@gmail.com"
        }
        response = self.client.post("/register/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
