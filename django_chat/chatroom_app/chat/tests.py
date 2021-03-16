from django.test import TestCase

# chat/tests.py

from django.test import TestCase

from .models import Room

class HomePageTest(TestCase):
    def test_all_rooms_are_rendered_in_homepage(self):
        Room.objects.create(
            name='room 1',
            slug='room-1',
            description='This is the 1st room'
        )
        Room.objects.create(
            name='room 2',
            slug='room-2',
            description='This is the 2nd room'
        )

        response = self.client.get('/')

        self.assertContains(response, 'room 1')
        self.assertContains(response, 'room 2')
