from django.test import TestCase

# Create your tests here.
from .models import CustomUser

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username='testuser', email='test@example.com')

    def test_username_content(self):
        user = CustomUser.objects.get(id=1)
        expected_object_name = f'{user.username}'
        self.assertEquals(expected_object_name, 'testuser')
