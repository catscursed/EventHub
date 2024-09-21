import uuid

from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from unidecode import unidecode

from .models import Event, Order
from .filters import EventFilter

User = get_user_model()


def manager_required(func):
    """
    Декоратор для проверки прав менеджера или администратора.
    """
    def wrapper(request, *args, **kwargs):
        if not (request.user.status == 2 or request.user.is_admin):
            messages.error(request, 'У вас нет доступа к этой странице')
            return redirect('index')
        return func(request, *args, **kwargs)
    return wrapper


def index_view(request):
    """
    Отображение главной страницы с основными мероприятиями.
    """
    events = Event.objects.filter(is_active=True, is_main=True).order_by('-created_date')[:2]
    return render(request, 'product/index.html', {'events': events})


@login_required
def event_detail_view(request, slug):
    """
    Детальная страница мероприятия.
    """
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            event_total = event.price * quantity
            current_user = request.user
            if event_total <= current_user.wallet:
                order = Order(
                    user=request.user,
                    event=event,
                    quantity=quantity,
                    total_price=event_total,
                )
                order.save()

                current_user.wallet -= event_total
                current_user.save()

                ticket_code = str(uuid.uuid4())
                if 'tickets' not in request.session:
                    request.session['tickets'] = []
                request.session['tickets'].append({
                    'title': event.title,
                    'event_date': event.event_date.strftime('%d.%m.%Y %H:%M'),
                    'location': event.location,
                    'ticket_code': ticket_code,
                    'logo_url': event.logo.url,
                })
                request.session.modified = True
                messages.success(request, 'Билет успешно куплен.')
            else:
                messages.error(request, 'У вас недостаточно средств')
        except ValueError:
            messages.error(request, 'Некорректное значение количества')

    return render(request, 'product/event-detail.html', {'event': event})


def user_profile_view(request):
    """
    Страница профиля пользователя.
    """
    user = request.user
    return render(request, 'product/profile.html', {'user': user})


# Закомментировано из-за ошибки
# @cache_page(60 * 15)
def event_list_view(request):
    """
    Страница со списком мероприятий с фильтрацией и пагинацией.
    """
    queryset = Event.objects.filter(is_active=True)
    if 'search' in request.GET and request.GET['search'].strip():
        search = request.GET['search']
        queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

    event_filter = EventFilter(request.GET, queryset=queryset)
    paginator = Paginator(event_filter.qs, 5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'product/event-listing.html', {
        'events': page_obj.object_list,
        'filter': event_filter,
        'page_obj': page_obj
    })


@login_required
def event_create_view(request):
    """
    Страница создания мероприятий (доступна и видна только менеджеру)
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        logo = request.FILES.get('logo')
        event_date = request.POST.get('event_date')
        duration = request.POST.get('duration')
        location = request.POST.get('location')
        available = request.POST.get('available')
        is_main = request.POST.get('is_main') == 'on'
        is_active = request.POST.get('is_active') == 'on'

        event = Event(
            title=title,
            description=description,
            price=price,
            logo=logo,
            event_date=event_date,
            duration=duration,
            location=location,
            available=available,
            is_main=is_main,
            is_active=is_active
        )

        # генерация уникального slag
        base_slug = slugify(unidecode(title))  # применение unidecode (из-за поддержки русского текста)
        unique_slug = base_slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1

        event.slug = unique_slug
        event.save()
        return redirect('event_list')

    return render(request, 'product/event_create.html')



@login_required
@manager_required
def event_update_view(request, slug):
    """
    Страница обновления мероприятия (только для менеджеров или администраторов).
    """
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        event.description = request.POST.get('description', event.description)
        event.location = request.POST.get('location', event.location)
        event.price = request.POST.get('price', event.price)
        event.available = request.POST.get('available', event.available)
        event.duration = request.POST.get('duration', event.duration)
        if 'logo' in request.FILES:
            event.logo = request.FILES['logo']
        event.save()
        messages.success(request, 'Мероприятие успешно обновлено.')
        return redirect('event_detail', slug=event.slug)

    return render(request, 'product/event_update.html', {'event': event})


@login_required
@manager_required
def event_delete_view(request, slug):
    """
    Страница удаления мероприятия (только для менеджеров или администраторов).
    """
    event = get_object_or_404(Event, slug=slug)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'product/event_confirm_delete.html', {'event': event})
