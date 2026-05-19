from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from courses.models import Application, COURSE_TYPES, STATUS_CHOICES

def panel_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_panel_admin:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

#Получение данных пользователей
@panel_required
def panel_index(request):
    qs = Application.objects.select_related('user').all()
    status_filter = request.GET.get('status', '')
    course_filter = request.GET.get('course_type', '')
    sort_by = request.GET.get('sort', '-created_at')

    if status_filter:
        qs = qs.filter(status=status_filter)
    if course_filter:
        qs = qs.filter(course_type=course_filter)

    allowed_sorts = {
        'created_at', '-created_at',
        'status', '-status',
        'user__login', '-user__login',
        'date', '-date',
    }
    if sort_by in allowed_sorts:
        qs = qs.order_by(sort_by)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'panel/index.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'course_filter': course_filter,
        'sort_by': sort_by,
        'status_choices': STATUS_CHOICES,
        'course_choices': COURSE_TYPES,
        'total_count': qs.count(),
    })

#изменение статуса заявки
@panel_required
def change_status(request, app_id):
    if request.method == 'POST':
        app = get_object_or_404(Application, pk=app_id)
        new_status = request.POST.get('status', '')
        valid_values = [s[0] for s in STATUS_CHOICES]
        if new_status in valid_values and new_status != app.status and app.can_advance():
            old_label = app.get_status_display()
            app.status = new_status
            app.save()
            messages.success(
                request,
                f'Статус заявки #{app_id} изменён: «{old_label}» → «{app.get_status_display()}»'
            )
    return redirect('panel:index')
