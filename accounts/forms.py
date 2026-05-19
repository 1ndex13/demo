#Формы регистрации и авторизации
import re
from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Минимум 8 символов',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'right',
            'title': 'Пароль должен содержать не менее 8 символов',
        }),
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        }),
    )

    class Meta:
        model = User
        fields = ['login', 'last_name', 'first_name', 'middle_name', 'phone', 'email']
        widgets = {
            'login': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Макс. 6 символов (a–z, A–Z, 0–9)',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'right',
                'title': 'Только латинские буквы и цифры, максимум 6 символов',
                'maxlength': '6',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество (необязательно)',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'right',
                'title': 'Формат: +7 (XXX) XXX-XX-XX',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.ru',
            }),
        }
        labels = {
            'login': 'Логин',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'phone': 'Телефон',
            'email': 'Email',
        }

    def clean_login(self):
        login = self.cleaned_data.get('login', '')
        if not re.match(r'^[a-zA-Z0-9]{1,6}$', login):
            raise forms.ValidationError(
                'Логин: только латинские буквы и цифры, максимум 6 символов'
            )
        return login

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', 'Пароли не совпадают')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        }),
    )
