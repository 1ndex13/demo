import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Логин: только латиница+цифры, макс 6 символов (для обычных пользователей).
    # Для администратора Admin26 — ограничение применяется только на форме регистрации.
    login = models.CharField('Логин', max_length=20, unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login

    def get_full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return ' '.join(p for p in parts if p).strip()

    @property
    def is_panel_admin(self):
        #проверка логина админа
        return self.login == 'Admin26'
