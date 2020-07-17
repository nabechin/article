import io
import os
import tempfile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from account.models import UserProfile, Relation
from article.models import Article, Comment, FavoriteArticle, FavoriteComment
from message.models import TalkRoom, Message
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


# defaultのユーザ情報をdbに登録
def create_user(user):
    return get_user_model().objects.create(**user)

# defaultのユーザのプロフィール情報をdbに登録


def create_user_profile(user):
    return UserProfile.objects.create(user=user,
                                      introduction='自己紹介テスト')


# defaultの記事をdbに登録
def create_article(user):
    return Article.objects.create(content='記事コンテンツテスト', user=user)


def create_comment(user):
    return Comment.objects.create(user=user, article=create_article(user), content='コメントコンテンツテスト')


def create_talk_room(last_message):
    return TalkRoom.objects.create(last_message=last_message)


""" 未ログイン時にユーザのプロフィールAPIにアクセスをするテスト """


class PublicUserProfileApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # 権限のないユーザはアクセスできないことをテスト
    def test_user_profile_api_need_authenticate(self):
        response = self.client.get('/api/user_profile/')
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
            '/api/user_profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 登録したユーザの自己紹介と名前をhttpのpatchメソッドで更新し、ステータスが200を返す
    # また、更新したプロフィール（自己紹介と名前）がdbに置き換わっていることをテスト
    def test_patch_user_name_and_introduction(self):
        user_profile_after_update = {
            'user.name': '更新後名前',
            'introduction': '更新後自己紹介'
        }
        response = self.client.patch(
            '/api/user_profile/'+str(self.user_profile.id)+'/', user_profile_after_update)
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
            '/api/user_profile/'+str(self.user_profile.id)+'/', user_profile_after_update, format='multipart')
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

    # viewから登録したRelation情報が作成されていることをテスト
    def test_post_relation(self):
        relation_info = {"follwer": self.user1.id, "target": self.user2.id}
        response = self.client.post(
            '/api/relation/', relation_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        is_exists = Relation.objects.filter(
            follower=self.user1.id, target=self.user2.id).exists()
        self.assertTrue(is_exists)

    # 指定のRelationレコードをhttpのdeleteメソッドで削除されていることをテスト
    def test_delete_relation(self):
        relation = Relation.objects.create(
            follower=self.user1, target=self.user2)
        relation_info = {"follower": self.user1.id, "target": self.user2.id}
        response = self.client.delete(
            '/api/relation/'+str(relation.id)+'/')
        is_exists = Relation.objects.filter(
            follower=relation_info["follower"], target=relation_info["target"]).exists()
        self.assertFalse(is_exists)


""" 未ログイン時にCommentAPIにアクセスするテスト """


class PublicCommentApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    # 権限のないユーザはアクセスできないことをテスト
    def test_comment_api_need_authenticate(self):
        response = self.client.get('/api/comment/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCommentApiTest(TestCase):
    def setUp(self):
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest'
                     }
        self.client = APIClient()
        self.user = create_user(user_info)
        self.article = create_article(self.user)
        self.client.force_authenticate(self.user)

    def test_retrieve_comment(self):
        comment = Comment.objects.create(
            article=self.article, user=self.user, content='コメントテスト')
        response = self.client.get('/api/comment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_comment(self):
        comment_info = {"article": self.article.id,
                        "user": self.user.id, "content": "テスト用コメント"}
        response = self.client.post('/api/comment/', comment_info)
        is_exists = Comment.objects.filter(
            article=comment_info['article'], user=comment_info['user']).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(is_exists)


class PublicFavoriteArticleApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_favorite_article_api_need_authenticate(self):
        response = self.client.get('/api/favorite_article/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFavoriteArticleApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest'
                     }
        self.user = create_user(user_info)
        self.article = create_article(self.user)
        self.client.force_authenticate(self.user)

    def test_retrieve_favorite_article(self):
        favorite_article = FavoriteArticle.objects.create(
            article=self.article, user=self.user
        )
        response = self.client.get('/api/favorite_article/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_favorite_article(self):
        favorite_article_info = {"article": self.article.id,
                                 "user": self.user.id
                                 }
        response = self.client.post(
            '/api/favorite_article/', favorite_article_info)
        is_exists = FavoriteArticle.objects.filter(
            article=favorite_article_info["article"], user=favorite_article_info["user"]
        ).exists()
        self.assertTrue(is_exists)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_favorite_article(self):
        favorite_article = FavoriteArticle.objects.create(
            article=self.article, user=self.user
        )
        response = self.client.delete(
            '/api/favorite_article/'+str(favorite_article.id)+'/')
        is_exists = FavoriteArticle.objects.filter(
            pk=favorite_article.id).exists()
        self.assertFalse(is_exists)


class PublicFavoriteCommentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_favorite_comment_api_need_authenticate(self):
        response = self.client.get('/api/favorite_comment/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFavoriteCommentApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest'
                     }
        self.user = create_user(user_info)
        self.comment = create_comment(self.user)
        self.client.force_authenticate(self.user)

    def test_retrieve_favorite_comment(self):
        FavoriteComment.objects.create(user=self.user, comment=self.comment)
        response = self.client.get('/api/favorite_comment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_favorite_comment(self):
        favorite_comment_info = {"user": self.user.id, "comment": self.comment.id
                                 }
        response = self.client.post(
            '/api/favorite_comment/', favorite_comment_info)
        is_exists = FavoriteComment.objects.filter(
            user=favorite_comment_info["user"], comment=favorite_comment_info["comment"]
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(is_exists)

    def test_delete_favorite_comment(self):
        favorite_comment = FavoriteComment.objects.create(
            user=self.user, comment=self.comment)
        response = self.client.delete(
            '/api/favorite_comment/'+str(favorite_comment.id)+'/')
        is_exists = FavoriteComment.objects.filter(pk=favorite_comment.id
                                                   ).exists()
        self.assertFalse(is_exists)


class PublicMessageApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_message_api_need_authenticate(self):
        response = self.client.get('/api/message/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMessageApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest'
                     }
        self.user = create_user(user_info)
        self.talk_room = create_talk_room('テストラストメッセージ')
        self.client.force_authenticate(self.user)

    def test_retrieve_message(self):
        Message.objects.create(talk_room=self.talk_room,
                               sender=self.user, body='テストボディー')
        response = self.client.get('/api/message/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_post_message(self):
        message_info = {"talk_room":self.talk_room.id,"sender":self.user.id,"body":"テストメッセージ"}
        response = self.client.post('/api/message/',message_info)
        is_exists = Message.objects.filter(talk_room=message_info["talk_room"])
        self.assertTrue(is_exists)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)




