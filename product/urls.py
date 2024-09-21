from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('detail/<slug:slug>/', views.event_detail_view, name='event_detail'),
    path('profile/', views.user_profile_view, name='profile'),
    path('event_list/', views.event_list_view, name='event_list'),
    path('event_create/', views.event_create_view, name='event_create'),
    path('event_update/<slug:slug>/', views.event_update_view, name='event_update'),
    path('event_delete/<slug:slug>/', views.event_delete_view, name='event_delete'),
]
