from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from user.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='아이디')
    nickname = forms.CharField(max_length=10, label='닉네임')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    profile_img = forms.ImageField(label='프로필 이미지(선택)', widget=forms.ClearableFileInput(), required=False)

    class Meta:
        model = User
        fields = ['email', 'nickname', 'password1', 'password2', 'profile_img']


    def __init__(self, *args, **kwargs):
        # SignupForm 을 재정의하여 모든 template class 속성을 'form-control' 로 지정
        super(SignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='이메일')
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'