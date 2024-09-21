from django.urls import path
from . import views

urlpatterns = [
    path('order_list/', views.order_list_view, name='order_list'),
]
