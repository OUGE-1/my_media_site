from django.shortcuts import render
from django.conf import settings
from .models import Collection, Video, Audio
from .services.netease import NetEaseMusicService, NetEaseAPIError


def home(request):
    collections = Collection.objects.all()

    total_collections = collections.count()
    total_videos = Video.objects.count()
    total_audios = Audio.objects.count()

    recent_videos = Video.objects.order_by('-uploaded_at')[:8]
    recent_audios = Audio.objects.order_by('-uploaded_at')[:8]

    recent_items = []
    for v in recent_videos:
        recent_items.append({
            'type': 'video',
            'title': v.title,
            'collection': v.collection,
            'uploaded_at': v.uploaded_at,
        })
    for a in recent_audios:
        recent_items.append({
            'type': 'audio',
            'title': a.title,
            'collection': a.collection,
            'uploaded_at': a.uploaded_at,
        })

    recent_items.sort(key=lambda x: x['uploaded_at'], reverse=True)
    recent_items = recent_items[:8]

    return render(request, 'player/home.html', {
        'collections': collections,
        'total_collections': total_collections,
        'total_videos': total_videos,
        'total_audios': total_audios,
        'recent_items': recent_items,
    })


def media_list(request):
    collections = Collection.objects.all()
    return render(request, 'player/media_list.html', {
        'collections': collections,
    })


def online_search(request):
    keyword = request.GET.get('q', '').strip()
    source = request.GET.get('source') or settings.DEFAULT_MUSIC_SOURCE
    mode = request.GET.get('mode') or 'jump'   # jump=跳转 | embed=外链播放

    results = []
    error = None

    if keyword:
        try:
            service = NetEaseMusicService(source=source)
            results = service.search_songs(keyword)
            if not results:
                error = '没有找到相关歌曲'
        except NetEaseAPIError as e:
            error = str(e)

    return render(request, 'player/online_search.html', {
        'keyword': keyword,
        'source': source,
        'mode': mode,
        'sources': settings.NETEASE_API_SOURCES,
        'collections': Collection.objects.all(),
        'results': results,
        'error': error,
    })