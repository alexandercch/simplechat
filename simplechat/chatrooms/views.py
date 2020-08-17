import redis
import json

from django.conf import settings
from django.shortcuts import render, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from .models import Room
from .constants import MAX_CHAT_HISTORY


def index(request):
    if request.user.is_authenticated:
        context = {'rooms': Room.objects.all()}
        return render(request, 'chatrooms/index.html', context=context)
    else:
        login_url = resolve_url('login-view')

        return HttpResponseRedirect(login_url)

@csrf_protect
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'chatrooms/login.html', {'error': True})
        else:
            login(request, user)
            index_url = resolve_url('index-view')

            return HttpResponseRedirect(index_url)

    return render(request, 'chatrooms/login.html', {'error': False})


def room(request, roomid):
    if request.user.is_authenticated:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        room_name = "room_{}".format(roomid)
        messages = ""
        for m in r.lrange(room_name, 0, MAX_CHAT_HISTORY):
            m = json.loads(m)
            messages = '{} :: {}\\n'.format(
                m['username'], m['message']) + messages
        room = Room.objects.get(id=roomid)
        return render(request, 'chatrooms/room.html',
            {'roomid': roomid, 'roomname': room.name, 'messages': messages}
        )
    else:
        login_url = resolve_url('login-view')

        return HttpResponseRedirect(login_url)


def user_logout(request):
    logout(request)
    login_url = resolve_url('login-view')
    return HttpResponseRedirect(login_url)

