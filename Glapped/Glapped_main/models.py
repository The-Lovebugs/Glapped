from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images', default='resources/default.jpg')
    category = models.CharField(max_length=255)
