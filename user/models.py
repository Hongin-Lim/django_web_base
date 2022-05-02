from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """User 에서 사용하기 위한 UserManager 생성"""

    def create_user(self, email, password=None, **extra_fields):
        """일반 유저로 생성할 경우"""
        if not email:
            raise ValueError('이메일을 입력해주세요')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """superuser 로 user 를 생성할 경우 필드값을 True 로 변경"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    nickname = models.CharField(max_length=30,unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to='profile', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
