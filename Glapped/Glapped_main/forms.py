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
    
    # Days 1-7 for auction length
    auction_length = forms.TypedChoiceField(
        label="Auction Length (Days)", 
        choices=[(i, str(i)) for i in range(1, 8)], 
        coerce=int,  # Ensures value is stored as an integer
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        starting_bid = cleaned_data.get("starting_bid")
        auction_length = cleaned_data.get("auction_length")

        # Ensure at least one of price or starting_bid is provided
        if not price and not starting_bid:
            raise forms.ValidationError("You must provide either a price (for Buy Now) or a starting bid (for Auction)!")

        # If price is provided, make sure auction-related fields are not present
        #if price and (starting_bid or auction_length):
            #raise forms.ValidationError("Cannot provide auction-related fields for a Buy Now listing!")

        # If starting_bid is provided, make sure auction_length is also provided
        if starting_bid and not auction_length:
            raise forms.ValidationError("Auction listings must have an auction length!")

        return cleaned_data



class ReportForm(forms.Form):
    REPORT_REASONS = [
        ('stolen_listing', 'Stolen Listing'),
        ('inappropriate_image', 'Inappropriate Image'),
        ('inappropriate_description', 'Inappropriate Description'),
        ('inappropriate_title', 'Inappropriate Title'),
        ('inappropriate_username', 'Inappropriate Username'),
    ]
    
    reason = forms.ChoiceField(
        label="Reason for Report",
        choices=REPORT_REASONS,
        required=True
    )
    description = forms.CharField(label="Extra detail", max_length=1000)
    link = forms.URLField(
        label="Link to Listing/User Profile",
        required=False
    )