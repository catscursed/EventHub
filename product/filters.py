import django_filters
from .models import Event
from django import forms


class EventFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Цена от'
    )
    price__lt = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Цена до'
    )
    event_date = django_filters.DateFilter(
        field_name='event_date',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата события'
    )

    class Meta:
        model = Event
        fields = ('price__gt', 'price__lt', 'event_date')
