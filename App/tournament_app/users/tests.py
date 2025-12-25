from django.test import TestCase
from .models import User

# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='Sherman Yee', email='yermanshee@gmail.com')
        User.objects.create(username='Darshan Health Club', email='dhc@gmail.com')

    def test_user_is_active(self):
        ''' Checks if newly created users are active and not admin'''

        sherman = User.objects.get(username="Sherman Yee")
        dhc = User.objects.get(username='Darshan Health Club')
        self.assertEqual(sherman.is_active, True)
        self.assertEqual(sherman.is_staff, False)
        self.assertEqual(dhc.is_active, True)