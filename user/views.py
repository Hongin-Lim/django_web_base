from django.contrib.auth import login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect

from user.forms import SignupForm, LoginForm
from user.models import User

import requests
import json


def signup(request):
    return render(request, 'user/signup.html')


def emailSignup(request):
    if request.method == "GET":
        return render(request, 'user/email_signup.html')
    elif request.method == "POST":
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            user = signupForm.save()
            token = PasswordResetTokenGenerator().make_token(user)

            message = 'http://127.0.0.1:8000/user/activate?email=' + user.email + '&token=' + token

            mail_title = "계정 활성화 확인 이메일"
            email = EmailMessage(mail_title, message, to=[user.email])
            email.send()
            return redirect('/user/login')


def userActivate(request):
    if request.method == "GET":
        email = request.GET.get('email', '')
        token = request.GET.get('token', '')

        user = User.objects.get(Q(email=email))

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'user/activated.html')
        else:
            return render(request, 'error.html')


def kakaoSignup(request):
    return redirect(
        'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=233c205674cdb37c23c7a2145c40b203&redirect_uri=https://97d7-125-133-75-24.ngrok.io/kakao/signup')


def kakaoSignupOauth(request):
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    data = {'grant_type': 'authorization_code',
            'client_id': '233c205674cdb37c23c7a2145c40b203',
            'redirect_uri': 'https://97d7-125-133-75-24.ngrok.io/kakao/signup',
            'code': request.GET.get('code')}
    res = requests.post('https://kauth.kakao.com/oauth/token',
                        data=data,
                        headers=headers)

    json_result = json.loads(res.text)

    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
               "Authorization": "Bearer " + json_result['access_token']}
    data = 'property_keys=["kakao_account.email", "properties.nickname"]'
    res = requests.post('https://kapi.kakao.com/v2/user/me', data=data, headers=headers)

    json_result = json.loads(res.text)

    email = json_result['kakao_account']['email']
    nickname = json_result['properties']['nickname']

    # 가입한 적 있으면 에러남, 에러처리 필요
    user = User()
    user.email = email
    user.nickname = nickname
    user.is_active = True
    user.save()

    return redirect('/user/login')


def kakaoLogin(request):
    return redirect(
        'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=233c205674cdb37c23c7a2145c40b203&redirect_uri=https://97d7-125-133-75-24.ngrok.io/kakao/login')


def kakaoLoginOauth(request):
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    data = {'grant_type': 'authorization_code',
            'client_id': '233c205674cdb37c23c7a2145c40b203',
            'redirect_uri': 'https://97d7-125-133-75-24.ngrok.io/kakao/login',
            'code': request.GET.get('code')}
    res = requests.post('https://kauth.kakao.com/oauth/token',
                        data=data,
                        headers=headers)

    json_result = json.loads(res.text)

    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
               "Authorization": "Bearer " + json_result['access_token']}
    data = 'property_keys=["kakao_account.email", "properties.nickname"]'
    res = requests.post('https://kapi.kakao.com/v2/user/me', data=data, headers=headers)

    json_result = json.loads(res.text)

    email = json_result['kakao_account']['email']

    # 카카오로 가입한 적 없으면 에러 발생, 에러처리 필요
    user = User.objects.get(Q(email=email))
    login(request, user)

    return redirect('/board/list')


def userunlink(request):
    return redirect(
        'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=233c205674cdb37c23c7a2145c40b203&redirect_uri=https://97d7-125-133-75-24.ngrok.io/kakao/unlink')


def kakaounlink(request):
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    data = {'grant_type': 'authorization_code',
            'client_id': '233c205674cdb37c23c7a2145c40b203',
            'redirect_uri': 'https://97d7-125-133-75-24.ngrok.io/kakao/unlink',
            'code': request.GET.get('code')}
    res = requests.post('https://kauth.kakao.com/oauth/token',
                        data=data,
                        headers=headers)

    print(res.text)
    json_result = json.loads(res.text)

    access_token = json_result['access_token']

    return render(request, 'user/unlink.html', {'access_token': access_token})


def userlogin(request):
    return render(request, 'user/login.html')


def userEmailLogin(request):
    if request.method == "GET":
        return render(request, 'user/email_login.html')
    elif request.method == "POST":
        loginForm = LoginForm(request, request.POST)
        if loginForm.is_valid():
            login(request, loginForm.get_user())
            return redirect('/board/list')
        else:
            return redirect('/user/login')


def userlogout(request):
    logout(request)
    return redirect('/user/login')