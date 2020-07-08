from django.test import TestCase, Client
from django.urls import reverse
from account.forms import UserRegisterForm

SIGNUP_URL = reverse("account:signup")


class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_user_account(self):
        user_info = {'name': "渡邉祐馬", 'email': "watawata@gmail.com",
                     'username': "yuma", 'password': "yumachin",
                     'password2': "yumachin"}
        response = self.client.post(SIGNUP_URL, user_info)
        self.assertEqual(response.status_code, 302)

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
