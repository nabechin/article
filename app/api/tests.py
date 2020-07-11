import io
import os
import tempfile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from account.models import UserProfile
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import UserProfileSerializer
from PIL import Image


def create_image_to_user_profile():
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image = Image.new('RGB', (100, 100))
    image.save(tmp_file.name)
    return tmp_file


def create_user_profile(user):
    return UserProfile.objects.create(user=user, introduction='自己紹介テスト')

# アプリケーションを利用していない場合にAPIにアクセスした際のテスト


class PublicUserProfileApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # 権限のないユーザはアクセスできないことをテスト
    def test_request_need_user_authenticate(self):
        response = self.client.get('/api/profileEdit/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserProfileApiTest(TestCase):

    def setUp(self):
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest'
                     }
        self.client = APIClient()
        self.user = get_user_model().objects.create(**user_info)
        self.client.force_authenticate(self.user)
        self.user_profile = create_user_profile(self.user)

    def tearDown(self):
        self.user_profile.profile_image.delete()
        self.user_profile.background_image.delete()

    def test_retrieve_user_profile(self):
        response = self.client.get(
            '/api/profileEdit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user_name_and_introduction(self):
        user_profile_after_update = {
            'user.name': '更新後名前',
            'introduction': '更新後自己紹介'
        }
        response = self.client.patch(
            '/api/profileEdit/'+str(self.user_profile.id)+'/', user_profile_after_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            user_profile_after_update['introduction'], response.data.get(
                'introduction'))
        self.assertEqual(
            user_profile_after_update['user.name'], response.data.get(
                'user').get('name'))

    def test_patch_profile_image_and_background_image(self):
        user_profile_after_update = {
            'user.name': '更新後名前',
            'profile_image': create_image_to_user_profile(),
            'background_image': create_image_to_user_profile(),
            'introduction': '更新前自己紹介'
        }
        response = self.client.patch(
            '/api/profileEdit/'+str(self.user_profile.id)+'/', user_profile_after_update, format='multipart')
        self.user_profile.refresh_from_db()
        self.user_profile = UserProfile.objects.get(pk=response.data.get('id'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profile_image', response.data)
        self.assertIn('background_image', response.data)
        self.assertTrue(os.path.exists(
            self.user_profile.profile_image.path))
        self.assertTrue(os.path.exists(
            self.user_profile.background_image.path))
