from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

#Регистрация пользователей
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('login', 'get_full_name', 'email', 'phone', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('login', 'email', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'email', 'phone')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('login', 'email', 'first_name', 'last_name', 'password1', 'password2')}),
    )
