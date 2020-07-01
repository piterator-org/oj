from django.test import TestCase

from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTests(TestCase):

    def test_create_profile_with_new_user(self):
        'Profile is saved automatically after User is created'
        user = User()
        user.save()
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.profile, Profile.objects.get(user=user))

    def test_profile_str_equals_user_str(self):
        'str(user.prifile) equals str(user)'
        user = User(username='username')
        user.save()
        self.assertEqual(str(user.profile), str(user))
