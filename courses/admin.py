from django.contrib import admin
from .models import Application, Review

#Заявки
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'get_course_type_display', 'date', 'status', 'created_at')
    list_filter = ('status', 'course_type')
    search_fields = ('user__login',)
    ordering = ('-created_at',)

#оТЗЫВЫ
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    ordering = ('-created_at',)
