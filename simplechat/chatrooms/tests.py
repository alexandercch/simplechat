from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url

from .models import Room

User = get_user_model()


class AuthorizedChatRoomAccessTest(TestCase):

    test_username = 'user1'
    test_password = 'password1'
    test_email = 'user1@mail.com'

    REDIRECTION_CODE = 302

    test_room_name = 'test_room'

    def setUp(self):
        User.objects.create_user(
            self.test_username, self.test_email, self.test_password)
        Room.objects.create(name=self.test_room_name)
        self.roomid = Room.objects.last().id

    def test_invalid_access(self):
        """
        Test if index and room view are accesible if user is not logged in,
        also these kind of request should be redirected to login view.
        """

        index_url = resolve_url('index-view')
        login_url = resolve_url('login-view')
        room_url = resolve_url('room-view', roomid=self.roomid)

        client = Client()

        response =  client.get(index_url)
        self.assertEqual(response.status_code, self.REDIRECTION_CODE)
        self.assertEqual(response['location'], login_url)

        response =  client.get(room_url)
        self.assertEqual(response.status_code, self.REDIRECTION_CODE)
        self.assertEqual(response['location'], login_url)
