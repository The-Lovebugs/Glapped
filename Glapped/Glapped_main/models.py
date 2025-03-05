from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


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

    description = models.TextField()
    image = models.ImageField(upload_to='product_images', default='resources/default.jpg')
    category = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

class BuyNowProduct(Product):
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='buyer')
    price = models.PositiveIntegerField(default=1)

class AuctionProduct(Product):
    start_time = models.DateTimeField(auto_now_add=True) # sets auction start time as the time the object is created
    end_time = models.DateTimeField()

    starting_bid = models.PositiveIntegerField(default=1)
    current_highest_bid = models.PositiveIntegerField(null=True, blank=True)
    current_highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name= 'highest_bidder')

    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name= 'winner' )

    def place_bid(self, user, bid_amount):
        # check that the new bid is higher than the current bid
        if self.current_highest_bid is not None and bid_amount <= self.current_highest_bid:
            raise ValueError("Bid must be higher than the current highest bid!")
        
        self.current_highest_bid = bid_amount
        self.current_highest_bidder = user
        self.save()

    def end_auction(self):
        if self.current_highest_bidder:
            self.winner = self.current_highest_bidder
            self.save()
        else:
            self.winner = None
            self.save()

