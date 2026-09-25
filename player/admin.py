from django.contrib import admin
from .models import Collection, Video, Audio

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'collection', 'uploaded_at')
    list_filter = ('collection',)
    search_fields = ('title',)

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'collection', 'uploaded_at')
    list_filter = ('collection',)
    search_fields = ('title', 'artist')
