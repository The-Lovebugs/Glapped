from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta


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
        ('misc', 'Miscellaneous')
    ]

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
    # Automatically set the start time to the current time
    start_time = models.DateTimeField(default=now) # Start time is automatically set to the current time
    auction_length = models.PositiveIntegerField(null=False, blank=False) # Auction length in days
    end_time = models.DateTimeField() # End time is calculated based on the auction length

    starting_bid = models.PositiveIntegerField()
    current_highest_bid = models.PositiveIntegerField(null=True, blank=True)
    current_highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='highest_bidder')

    sold = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')

    def save(self, *args, **kwargs):
        if not self.end_time:  # Only calculate end_time if it's not already set
            self.end_time = self.start_time + timedelta(days=self.auction_length)
        super(AuctionProduct, self).save(*args, **kwargs)


    def place_bid(self, user, bid_amount):
        # Check that the new bid is higher than the current bid
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
