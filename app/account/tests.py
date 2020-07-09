from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
from account.forms import UserRegisterForm, LoginForm


SIGNUP_URL = reverse('account:signup')
LOGIN_URL = reverse('account:login')
LOGOUT_URL = reverse('account:logout')

# ユーザ登録テスト


class UserRegisterTest(TestCase):
    # viewからのダミーアクセスを可能にするオブジェクトの設定

    def setUp(self):
        self.client = Client()

    # viewからアカウント情報を入力し、アカウント作成の完了を意味するステータスコート302を返すことをテスト
    def test_regist_user_account(self):
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest',
                     'password2': 'testtest'}
        response = self.client.post(SIGNUP_URL, user_info)
        self.assertEqual(response.status_code, 302)

    # メールアドレスが正規化されていることのテスト
    def test_user_email_normarize(self):
        user_info = {'name': 'テスト１', 'email': 'test1@GMAIL.COM',
                     'username': 'test1', 'password': 'testtest',
                     }
        user = get_user_model().objects.create_user(**user_info)
        self.assertEqual(user.email, user_info['email'].lower())

    # モデルに入力した値が期待する値であるかの確認
    def test_create_correct_model(self):
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest',
                     }
        user = get_user_model().objects.create_user(**user_info)
        self.assertEqual(user.name, user_info['name'])
        self.assertEqual(user.email, user_info['email'])
        self.assertEqual(user.username, user_info['username'])
        self.assertTrue(user.check_password(user_info['password']))

    # 空のアカウント情報を入力したときに、期待するエラーメッセージが返ってくることのテスト
    def test_create_user_account_without_all_infomation(self):
        user_info = {'name': '', 'email': '',
                     'username': '', 'password': '',
                     'password2': ''}
        form = UserRegisterForm(user_info)
        form.is_valid()
        self.assertTrue('名前を入力してください' in form.errors['name'])
        self.assertTrue('メールアドレスを入力してください' in form.errors['email'])
        self.assertTrue('ユーザ名を入力してください' in form.errors['username'])
        self.assertTrue('パスワードは英数字8文字以上で入力してください' in form.errors['password'])

    # パスワードと確認用パスワードが異なった場合に期待するエラーメッセージが返ってくることのテスト
    def test_get_error_password_differ_from_password2(self):
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest',
                     'password2': 'testaaatest'}
        form = UserRegisterForm(user_info)
        form.is_valid()
        self.assertTrue('パスワードと確認用パスワードが一致しません' in form.errors['__all__'])

    # すでに同じユーザ名とメールアドレスで登録されているユーザがいた場合エラーとするテスト
    def test_not_register_same_username_or_email(self):
        user_info_first = {'name': 'テスト１', 'email': 'test1@gmail.com',
                           'username': 'test1', 'password': 'testtest',
                           'password2': 'testtest'}
        user_info_second = {'name': 'テスト２', 'email': 'test1@gmail.com',
                            'username': 'test1', 'password': 'testtest1',
                            'password2': 'testtest1'}
        form = UserRegisterForm(user_info_first)
        user = form.save()
        user.refresh_from_db()
        form = UserRegisterForm(user_info_second)
        # すでに登録されているユーザ名とメールアドレスでアカウントを作成するため、ValueError
        with self.assertRaises(ValueError):
            user = form.save()


# ログイン情報入力テスト


class LoginUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        user_info = {'name': 'テスト１', 'email': 'test1@gmail.com',
                     'username': 'test1', 'password': 'testtest',
                     }
        get_user_model().objects.create_user(**user_info)

    # 登録されていないメールアドレスでログインした時にエラーを出すテスト
    def test_login_email_error(self):
        user_login_form = {'username': 'test2@gmail.com',
                           'password': 'testtest'
                           }
        form = LoginForm(data=user_login_form)
        self.assertFalse(form.is_valid())

    # 登録されていないパスワードでログインした時にエラーを出すテスト
    def test_login_password_error(self):
        user_login_form = {'username': 'test1@gmail.com',
                           'password': 'testtesttest'
                           }
        form = LoginForm(data=user_login_form)
        self.assertFalse(form.is_valid())

    # ログイン、ログアウト成功のテスト
    def test_login_and_logout_success(self):
        user_login_form = {'username': 'test1@gmail.com',
                           'password': 'testtest'
                           }

        # ログイン後、ユーザにアクセス権限があればログイン成功
        response = self.client.post(LOGIN_URL, user_login_form)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        # ログアウト後、ユーザにアクセス権限がなければログアウト成功
        response = self.client.post(LOGOUT_URL)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
