#Вьюхи
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, Review
from .forms import ApplicationForm, ReviewForm


def home_view(request):
    return render(request, 'home.html')

#Личный кабинет
@login_required
def cabinet_view(request):
    if request.user.is_panel_admin:
        return redirect('panel:index')

    applications = request.user.applications.all()
    reviews = request.user.reviews.select_related('application').all()
    completed_without_review = applications.filter(status='completed', review__isnull=True)
    review_form = ReviewForm()

    return render(request, 'courses/cabinet.html', {
        'applications': applications,
        'reviews': reviews,
        'completed_without_review': completed_without_review,
        'review_form': review_form,
    })

#Заявка
@login_required
def apply_view(request):
    if request.user.is_panel_admin:
        return redirect('panel:index')

    form = ApplicationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.save()
        messages.success(request, f'Заявка #{application.pk} успешно подана! Статус: «Новая».')
        return redirect('courses:cabinet')

    return render(request, 'courses/apply.html', {'form': form})

#Отзыв
@login_required
def add_review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            app_id = request.POST.get('application_id')
            if app_id:
                app = get_object_or_404(
                    Application, pk=app_id, user=request.user, status='completed'
                )
                if Review.objects.filter(application=app).exists():
                    messages.error(request, 'Отзыв на этот курс уже оставлен.')
                    return redirect('courses:cabinet')
                review.application = app
            review.save()
            messages.success(request, 'Отзыв успешно добавлен. Спасибо!')
        else:
            messages.error(request, 'Ошибка при добавлении отзыва. Проверьте поля.')
    return redirect('courses:cabinet')
