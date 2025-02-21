from django.db import models
from django.contrib.auth.models import User

# UserProfile model with points
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
