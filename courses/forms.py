import datetime
from django import forms
from .models import Application, Review

#Форма заявок
class ApplicationForm(forms.ModelForm):
    date = forms.DateField(
        label='Дата начала',
        input_formats=['%d.%m.%Y'],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ДД.ММ.ГГГГ',
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'right',
            'title': 'Введите дату в формате ДД.ММ.ГГГГ',
            'maxlength': '10',
        }),
        error_messages={'invalid': 'Введите дату в формате ДД.ММ.ГГГГ'},
    )

    class Meta:
        model = Application
        fields = ['course_type', 'date', 'payment_method']
        widgets = {
            'course_type': forms.Select(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'right',
                'title': 'Выберите тип курса',
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'right',
                'title': 'Выберите удобный способ оплаты',
            }),
        }
        labels = {
            'course_type': 'Тип курса',
            'payment_method': 'Способ оплаты',
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < datetime.date.today():
            raise forms.ValidationError('Дата начала не может быть в прошлом. Выберите сегодня или позже.')
        return date

#Форма отзывов
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь впечатлениями о курсе...',
            }),
            'rating': forms.Select(
                choices=[(i, f'{i} {"звезда" if i == 1 else "звезды" if i < 5 else "звёзд"}') for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
        }
        labels = {
            'text': 'Ваш отзыв',
            'rating': 'Оценка',
        }
