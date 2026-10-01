import socket
from django.contrib.auth.models import User


def user_box(request):
    users = User.objects.order_by('username')
    return {'all_users': users}


def lan_ip(request):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = '127.0.0.1'
    return {'lan_ip': ip}