#Вьюхи: регистрация, вход, выход.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('courses:cabinet')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Регистрация завершена! Войдите в систему.')
        return redirect('accounts:login')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_panel_admin:
            return redirect('panel:index')
        return redirect('courses:cabinet')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login_val = form.cleaned_data['login']
        password = form.cleaned_data['password']
        user = authenticate(request, username=login_val, password=password)
        if user:
            login(request, user)
            if user.is_panel_admin:
                return redirect('panel:index')
            return redirect('courses:cabinet')
        messages.error(request, 'Неверный логин или пароль. Проверьте данные и попробуйте снова.')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Вы вышли из системы.')
    return redirect('home')
