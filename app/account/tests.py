from django.test import TestCase, Client
from django.urls import reverse
from account.forms import UserRegisterForm
from django.contrib.auth import get_user_model


SIGNUP_URL = reverse("account:signup")


class UserRegisterViewTest(TestCase):
    '''viewからのダミーアクセスを可能にするオブジェクトの設定'''

    def setUp(self):
        self.client = Client()

    '''viewからアカウント情報を入力し、アカウント作成の完了を意味するステータスコート302を返すことをテスト'''

    def test_regist_user_account(self):
        user_info = {'name': "渡邉祐馬", 'email': "watawata@gmail.com",
                     'username': "yuma", 'password': "yumachin",
                     'password2': "yumachin"}
        response = self.client.post(SIGNUP_URL, user_info)
        self.assertEqual(response.status_code, 302)

    '''メールアドレスが正規化されていることのテスト'''

    def test_user_email_normarize(self):
        user_info = {'name': "渡邉祐馬", 'email': "watawata@GMAIL.COM",
                     'username': "yuma", 'password': "yumachin",
                     }
        user = get_user_model().objects.create_user(**user_info)
        self.assertEqual(user.email, user_info['email'].lower())

    '''モデルに入力した値が期待する値であるかの確認'''

    def test_create_correct_model(self):
        user_info = {'name': "渡邉祐馬", 'email': "watawata@gmail.com",
                     'username': "yuma", 'password': "yumachin",
                     }
        user = get_user_model().objects.create_user(**user_info)
        self.assertEqual(user.name, user_info['name'])
        self.assertEqual(user.email, user_info['email'])
        self.assertEqual(user.username, user_info['username'])
        self.assertTrue(user.check_password(user_info['password']))

    '''空のアカウント情報を入力したときに、期待するエラーメッセージが返ってくることのテスト'''

    def test_create_user_account_without_all_infomation(self):
        user_info = {'name': "", 'email': "",
                     'username': "", 'password': "",
                     'password2': ""}
        form = UserRegisterForm(user_info)
        form.is_valid()
        self.assertTrue('名前を入力してください' in form.errors['name'])
        self.assertTrue('メールアドレスを入力してください' in form.errors['email'])
        self.assertTrue('ユーザ名を入力してください' in form.errors['username'])
        self.assertTrue('パスワードは英数字8文字以上で入力してください' in form.errors['password'])

    '''パスワードと確認用パスワードが異なった場合に期待するエラーメッセージが返ってくることのテスト'''

    def test_get_error_password_differ_from_password2(self):
        user_info = {'name': "渡邉祐馬", 'email': "watawata@gmail.com",
                     'username': "yuma", 'password': "yumachin",
                     'password2': "nabechin"}
        form = UserRegisterForm(user_info)
        form.is_valid()
        self.assertTrue('パスワードと確認用パスワードが一致しません' in form.errors['__all__'])

    '''すでに同じユーザ名とメールアドレスで登録されているユーザがいた場合エラーとするテスト'''
    def test_not_register_same_username_or_email(self):
        user_info_first = {'name': "渡邉祐馬", 'email': "watawata@gmail.com",
                           'username': "yuma", 'password': "yumachin",
                           'password2': "yumachin"}
        user_info_second = {'name': "わたなべゆうま", 'email': "watawata@gmail.com",
                            'username': "yuma", 'password': "uuuuuuuuuu",
                            'password2': "uuuuuuuuuu"}
        form = UserRegisterForm(user_info_first)
        user = form.save()
        user.refresh_from_db()
        form = UserRegisterForm(user_info_second)
        '''すでに登録されているユーザ名とメールアドレスでアカウントを作成するため、ValueError'''
        with self.assertRaises(ValueError):
            user = form.save()
