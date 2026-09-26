from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('media/', views.media_list, name='media_list'),
    path('lyric/<int:audio_id>/', views.lyric_detail, name='lyric_detail'),   # ← 改了这里
    path('online/', views.online_search, name='online_search'),

    path('api/song-url/<int:song_id>/', views.api_get_song_url, name='api_get_song_url'),
    path('api/lyric/<int:song_id>/', views.api_get_lyric, name='api_get_lyric'),
]