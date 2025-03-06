from django import forms
from django.core.validators import MinValueValidator

class CreateNewListing(forms.Form):
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
    
    # Fields for both BuyNowProduct and AuctionProduct
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(label="Description", max_length=1000)
    category = forms.ChoiceField(
        label="Category",
        choices=CATEGORY_CHOICES,
        required=True
    )
    image = forms.ImageField(label= "Image", required=True)


    # Fields for only BuyNowProduct
    price = forms.IntegerField(
        label="Price", 
        validators=[MinValueValidator(1)],
        required=False
    )

    # Fields for only AuctionProduct
    starting_bid = forms.IntegerField(
        label="Starting Bid",
        validators=[MinValueValidator(1)],
        required=False
    )
    
    # Auction length field (1 to 7 days)
    auction_length = forms.ChoiceField(
        label="Auction Length (Days)", 
        choices=[(str(i), str(i)) for i in range(1, 8)], 
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        starting_bid = cleaned_data.get("starting_bid")
        auction_length = cleaned_data.get("auction_length")

        # Validation
        if not price and not starting_bid:
            raise forms.ValidationError("You must provide either a price (for Buy Now) or a starting bid (for Auction)!")

        if price and (starting_bid or auction_length):
            raise forms.ValidationError("Cannot provide auction-related fields for a Buy Now listing!")

        if starting_bid and not auction_length:
            raise forms.ValidationError("Auction listings must have an auction length!")

        return cleaned_data
