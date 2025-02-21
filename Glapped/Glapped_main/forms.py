from django import forms
from django.core.validators import MinValueValidator

class CreateNewListing(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(label="Description", max_length=1000)
    price = forms.IntegerField(
        label="Price", 
        validators=[MinValueValidator(1)],  # Ensures value is at least 1
    )
    image = forms.ImageField(label= "Image", required=True)