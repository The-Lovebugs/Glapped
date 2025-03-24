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

    reportAmount = models.PositiveIntegerField(default=0)
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
CATEGORY_SAVINGS = {
    'tshirt': {'water': 2700, 'co2': 6},
    'button_up': {'water': 3000, 'co2': 7},
    'vest': {'water': 1800, 'co2': 4},
    'sweater': {'water': 6000, 'co2': 20},
    'hoodie': {'water': 8100, 'co2': 21},
    'cardigan': {'water': 5500, 'co2': 18},
    'denim_jacket': {'water': 9000, 'co2': 25},
    'leather_jacket': {'water': 17000, 'co2': 45},
    'winter_coat': {'water': 12000, 'co2': 30},
    'blazer': {'water': 8000, 'co2': 22},
    'jeans': {'water': 7600, 'co2': 33},
    'cargo_trousers': {'water': 7000, 'co2': 28},
    'suit_trousers': {'water': 6000, 'co2': 20},
    'shorts': {'water': 4000, 'co2': 10},
    'skirt': {'water': 3500, 'co2': 8},
    'dress': {'water': 7000, 'co2': 25},
    'trainers': {'water': 4400, 'co2': 15},
    'leather_shoes': {'water': 8500, 'co2': 25},
    'sandals': {'water': 2500, 'co2': 5},
    'flip_flops': {'water': 1500, 'co2': 3},
    'boots': {'water': 10000, 'co2': 30},
    'hat': {'water': 1200, 'co2': 3},
    'scarf': {'water': 1000, 'co2': 2},
    'gloves': {'water': 2000, 'co2': 5},
    'tie': {'water': 1500, 'co2': 4},
    'jewelry': {'water': 800, 'co2': 2},
    'sportswear': {'water': 3000, 'co2': 10},
    'accessories': {'water': 1000, 'co2': 3},
    'misc': {'water': 1000, 'co2': 5},  # fallback/default
}


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

    
class ListingReport(models.Model):
    CATEGORY_CHOICES = [("Inappropriate conduct"),("Misleading content"),("Fraudulent behaviour"),("Fake listing"),("User safety")]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reports')
    category = models.CharField(max_length=255)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
