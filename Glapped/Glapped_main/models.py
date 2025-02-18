from django.db import models

# Create your models here.



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    #image = models.ImageField(upload_to='product_images')
    category = models.CharField(max_length=255)

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    