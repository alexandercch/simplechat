from django.shortcuts import render, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

from .models import Room

def index(request):
    if request.user.is_authenticated:
        context = {
            'rooms': Room.objects.all() 
        }
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
        return render(request, 'chatrooms/room.html', {'roomid': roomid})
    else:
        login_url = resolve_url('login-view')

        return HttpResponseRedirect(login_url)


def user_logout(request):
    logout(request)
    login_url = resolve_url('login-view')
    return HttpResponseRedirect(login_url)

