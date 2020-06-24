from django import forms
from django.contrib.auth import get_user_model
import re
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('name','email','username','password')
        widgets = {
                    'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                  } 

    password2 = forms.CharField(
        label='確認用パスワード',
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
    )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Name'}
        self.fields['name'].label = '名前'
        self.fields['name'].required = False
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Email'}
        self.fields['email'].label = 'メールアドレス'
        self.fields['email'].required = False
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'Username'}
        self.fields['username'].label = 'ユーザ名'
        self.fields['username'].required = False
        self.fields['password'].label = 'パスワード'
        self.fields['password'].required = False


    def clean_name(self):
        name = self.cleaned_data['name'] 
        if not name:
            raise forms.ValidationError('名前を入力してください')
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('メールアドレスを入力してください')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError('ユーザ名を入力してください')
        return username
    
    def clean_password(self):
        alphaReg = re.compile(r'^[a-zA-Z0-9]+$')
        password = self.cleaned_data['password'] 
        if len(password) < 7 or not alphaReg.match(password):
            raise forms.ValidationError('パスワードは英数字8文字以上で入力してください')
        return password

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password') 
        if not password:
            return 
        password2 = self.cleaned_data.get('password2') 
        if password != password2:
            raise forms.ValidationError('パスワードと確認用パスワードが一致しません')


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("ログインに失敗しました。"
                           "メールアドレスとパスワードを確認してください"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'   
            field.widget.attrs['placeholder'] = field.label 
            field.widget.label = field.label
            field.required = False
