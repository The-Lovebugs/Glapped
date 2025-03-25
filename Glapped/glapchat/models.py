from django.db import models
from django.contrib.auth.models import User
from Glapped_main.models import Product
import uuid

# Create your models here.


class Message(models.Model):
    message = models.CharField(max_length=1000, default='Message')
    sender = models.ForeignKey(User, name='sender', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.message

class Room(models.Model):
    ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='seller')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
