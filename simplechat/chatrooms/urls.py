from django.urls import path, include

from .views import user_login, index, room, user_logout


urlpatterns = [
    path('', index, name='index-view'),
    path('room/<int:roomid>/', room, name='room-view'),
    path('login/', user_login, name='login-view'),
    path('logout/', user_logout, name='logout-view'),
]
