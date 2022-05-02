"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import board.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', board.views.home),
    path('board/like/<int:bid>', board.views.like),
    path('board/register', board.views.register),
    path('board/list', board.views.posts),
    path('board/read/<int:bid>', board.views.read),
    path('board/delete/<int:bid>', board.views.delete),
    path('board/update/<int:bid>', board.views.update),
    path('user/signup', user.views.signup),
    path('user/emailsignup', user.views.emailSignup),
    path('user/kakaosignup', user.views.kakaoSignup),
    path('kakao/signup', user.views.kakaoSignupOauth),
    path('user/unlink', user.views.userunlink),
    path('kakao/unlink', user.views.kakaounlink),
    path('user/activate', user.views.userActivate),
    path('user/login', user.views.userlogin),
    path('user/emaillogin', user.views.userEmailLogin),
    path('user/kakaologin', user.views.kakaoLogin),
    path('kakao/login', user.views.kakaoLoginOauth),
    path('user/logout', user.views.userlogout),
]
