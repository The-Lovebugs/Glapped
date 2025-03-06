from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Product(models.Model):
    CATEGORY_CHOICES = [
    # Tops
    ('tshirt', 'T-Shirt'),
    ('button_up', 'Button-Up Shirt'),
    ('vest', 'Vest'),
    ('sweater', 'Sweater'),
    ('hoodie', 'Hoodie'),
    ('cardigan', 'Cardigan'),

    # Outerwear
    ('denim_jacket', 'Denim Jacket'),
    ('leather_jacket', 'Leather Jacket'),
    ('winter_coat', 'Winter Coat'),
    ('blazer', 'Blazer'),

    # Bottoms
    ('jeans', 'Jeans'),
    ('cargo_trousers', 'Cargo Trousers'),
    ('suit_trousers', 'Suit Trousers'),
    ('shorts', 'Shorts'),
    ('skirt', 'Skirt'),
    ('dress', 'Dress'),

    # Footwear
    ('trainers', 'Trainers'),
    ('leather_shoes', 'Leather Shoes'),
    ('sandals', 'Sandals'),
    ('flip_flops', 'Flip Flops'),
    ('boots', 'Boots'),

    # Accessories
    ('hat', 'Hat'),
    ('scarf', 'Scarf'),
    ('gloves', 'Gloves'),
    ('tie', 'Tie'),
    ('jewelry', 'Jewelry'),

    # Other categories
    ('sportswear', 'Sportswear'),
    ('accessories', 'Accessories'),
    ('misc', 'Miscellaneous')]

    name = models.CharField(max_length=255, default='Product')

    price = models.PositiveIntegerField(default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images', default='resources/default.jpg')
    category = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='buyer')
    #where count of reports will be
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
