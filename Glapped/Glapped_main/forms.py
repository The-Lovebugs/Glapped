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
    
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(label="Description", max_length=1000)
    price = forms.IntegerField(
        label="Price", 
        validators=[MinValueValidator(1)],  # Ensures value is at least 1
    )
    image = forms.ImageField(label= "Image", required=True)

    category = forms.ChoiceField(
        label="Category",
        choices=CATEGORY_CHOICES,
        required=True
    )