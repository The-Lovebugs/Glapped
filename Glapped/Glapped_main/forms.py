from django import forms

class CreateNewListing(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(label="Description", max_length=1000)
    price = forms.DecimalField(label="Price", max_digits=8, decimal_places=2)
    image = forms.ImageField(label= "Image", required=True)