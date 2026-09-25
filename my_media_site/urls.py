from django.contrib import admin
from django.urls import path, include
from player.range_views import serve_media

urlpatterns = [
    path('admin/', admin.site.urls),
    # 支持 Range 的媒体文件服务
    path('media/<path:path>', serve_media, name='serve_media'),
    path('', include('player.urls')),
]

# 【删除】下面这几行不再需要
# from django.conf import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)