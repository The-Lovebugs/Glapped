from django.test import TestCase
from .models import Product
from .forms import CreateNewListing


class ProductTestCase(TestCase):   
    def setUp(self):
        self.productdetails = {
            'title': 'Blue Jeans',
            'price': 50,
            'description': 'Hole over left knee',
            'image': 'resources/default.jpg'}
    def test_form(self):
        form = CreateNewListing(data=self.productdetails)
        instances = Product.objects.all()
        print("\nPrinting all MyModel instances:")
        for instance in instances:
            print(instance.name)
        self.assertTrue(form.is_valid())
    def test_createListing(self):
        # send product data
        self.client.post('/createlisting/', self.productdetails, follow=True)
        # Check if the user is created in the database
        instances = Product.objects.all()
        print("\nPrinting all MyModel instances:")
        for instance in instances:
            print(instance)
        self.assertTrue(Product.objects.filter(name=self.productdetails['title']).exists())