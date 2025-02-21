from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

# Create your tests here.
class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'P455word!'}
        self.client.post('/register/', self.credentials, follow=True)
    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
    def test_account_created(self):
        # Check if the user is created in the database
        self.assertTrue(User.objects.filter(username=self.credentials['username']).exists()) 
    def test_userprofile_created(self):
        # reference created user account
        user = User.objects.get(username=self.credentials['username'])
        #test is userprofile has been created
        try:
            #testing if userprofile exists
            profile = UserProfile.objects.get(user=user)
            self.assertIsNotNone(profile)
        except UserProfile.DoesNotExist:
            self.fail("UserProfile was not created for the user.")