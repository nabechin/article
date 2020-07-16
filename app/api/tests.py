import io
import os
import tempfile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from account.models import UserProfile, Relation
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import UserProfileSerializer
from PIL import Image


# ユーザのプロフィール登録、更新の際に利用する画像を作成するメソッド
def create_image_to_user_profile():
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image = Image.new('RGB', (100, 100))
    image.save(tmp_file.name)
    return tmp_file


# defaultでユーザ情報をdbに登録
def create_user(user_info):
    return get_user_model().objects.create(**user_info)

# defaultでユーザのプロフィール情報をdbに登録


def create_user_profile(user):
    return UserProfile.objects.create(user=user, introduction='自己紹介テスト')


""" 未ログイン時にユーザのプロフィールAPIにアクセスをするテスト """


class PublicUserProfileApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # 権限のないユーザはアクセスできないことをテスト
    def test_user_profile_api_need_authenticate(self):
        response = self.client.get('/api/profileEdit/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


""" ログイン時にユーザのプロフィールAPIにアクセスをするテスト """


class PrivateUserProfileApiTest(TestCase):
    # テストの前にユーザをdbに登録し、ログイン状態する
    def setUp(self):
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest'
                     }
        self.client = APIClient()
        self.user = get_user_model().objects.create(**user_info)
        self.client.force_authenticate(self.user)
        self.user_profile = create_user_profile(self.user)

    # テスト様に登録した画像がフォルダに残らないよう、テストメソッドの実行終了ごとに画像を削除する
    def tearDown(self):
        self.user_profile.profile_image.delete()
        self.user_profile.background_image.delete()

    # 登録したユーザの自己紹介と名前をhttpのgetメソッドで呼びだし、ステータスが200を返す
    def test_retrieve_user_profile(self):
        response = self.client.get(
            '/api/profileEdit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 登録したユーザの自己紹介と名前をhttpのpatchメソッドで更新し、ステータスが200を返す
    # また、更新したプロフィール（自己紹介と名前）がdbに置き換わっていることをテスト
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

    # 登録したユーザのプロフィール画像と背景画像をhttpのpatchメソッドで更新し、ステータスが200を返す
    # また、更新したがプロフィール画像と背景画像がdbに置き換わっていることをテスト
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


""" 未ログイン時にユーザ同士のRelationAPIにアクセスするテスト """


class PublicRelationApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # 権限のないユーザはアクセスできないことをテスト
    def test_relation_api_need_authenticate(self):
        response = self.client.get('/api/relation/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


""" ログイン時にユーザ同士のRelationAPIにアクセスするテスト """


class PrivateRelationApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # ユーザ情報をテストの前に登録する
        self.user_info_1 = {'name': 'テスト１', 'email': 'test1@gmail.com',
                            'username': 'test1', 'password': 'testtest1'
                            }
        self.user_info_2 = {'name': 'テスト2', 'email': 'test2@gmail.com',
                            'username': 'test2', 'password': 'testtest2'
                            }
        self.user1 = create_user(self.user_info_1)
        self.user2 = create_user(self.user_info_2)
        self.client.force_authenticate(self.user1)

    # RelationTableに登録したデータをhttpのgetメソッドで取得できることをテスト
    def test_retrieve_relation(self):
        relation = Relation.objects.create(
            follower=self.user1, target=self.user2)
        relation.refresh_from_db()
        response = self.client.get('/api/relation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_relation(self):
        response = self.client.post(
            '/api/relation/', {"target": self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
