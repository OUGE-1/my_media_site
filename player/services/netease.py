import requests
from django.conf import settings


class NetEaseAPIError(Exception):
    pass


# 伪装成浏览器，避免被 API 服务器识别为爬虫
DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Referer': 'https://music.163.com/',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


class NetEaseMusicService:
    def __init__(self, source=None):
        self.sources = settings.NETEASE_API_SOURCES
        if source and source != 'auto' and source in self.sources:
            self.preferred = [source]
        else:
            self.preferred = list(self.sources.keys())

    def _request(self, path, params, timeout=6):
        last_error = None
        for key in self.preferred:
            base = self.sources[key]['url']
            try:
                resp = requests.get(
                    f'{base}{path}',
                    params=params,
                    headers=DEFAULT_HEADERS,
                    timeout=timeout,
                )
                resp.raise_for_status()
                return resp.json()
            except (requests.RequestException, ValueError) as e:
                last_error = f'{key}: {e}'
                continue
        raise NetEaseAPIError(f'所有音乐源均失败：{last_error}')

    def search_songs(self, keyword, limit=20):
        data = self._request('/search', {'keywords': keyword, 'limit': limit})
        songs = data.get('result', {}).get('songs', []) or []
        return [self._simplify(s) for s in songs]

    @staticmethod
    def _simplify(song):
        artists = song.get('artists') or song.get('ar') or []
        album = song.get('album') or song.get('al') or {}
        ms = song.get('duration') or song.get('dt') or 0

        # 毫秒 → 分:秒
        minutes, seconds = divmod(ms // 1000, 60)
        sid = song.get('id')

        return {
            'id': sid,
            'name': song.get('name'),
            'artist': ' / '.join(a.get('name', '') for a in artists),
            'album': album.get('name', ''),
            'cover': album.get('picUrl', ''),
            'duration_text': f'{minutes}:{seconds:02d}' if ms else '',
            # 跳转用：外链播放页（新窗口打开）
            'web_url': f"https://music.163.com/#/outchain/2/{sid}/m/use/html",
            # 外链播放用：iframe 地址（页内播放）
            'player_src': f"//music.163.com/outchain/player?type=2&id={sid}&auto=1&height=66",
        }