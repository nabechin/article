from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import UserProfileSerializer



class PublicUserProfileApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_request_need_user_authenticate(self):
        response = self.client.get('/api/profileEdit')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
