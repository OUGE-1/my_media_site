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
    list_display = ('title', 'artist', 'collection', 'has_lyric', 'uploaded_at')
    list_filter = ('collection',)
    search_fields = ('title', 'artist')

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'artist', 'file', 'collection')
        }),
        ('歌词（LRC 格式）', {
            'fields': ('lyric',),
            'description': '格式：[00:12.50]歌词文本，每行一句',
        }),
    )

    def has_lyric(self, obj):
        return '✓' if obj.lyric else '—'
    has_lyric.short_description = '有歌词'