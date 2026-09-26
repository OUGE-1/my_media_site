from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('media/', views.media_list, name='media_list'),
    path('online/', views.online_search, name='online_search'),
]