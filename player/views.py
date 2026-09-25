from django.shortcuts import render
from .models import Collection

def media_list(request):
    collections = Collection.objects.prefetch_related('videos', 'audios').all()
    return render(request, 'player/media_list.html', {'collections': collections})
