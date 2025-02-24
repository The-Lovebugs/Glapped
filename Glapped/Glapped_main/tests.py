from django.test import TestCase
from .models import Product
from .forms import CreateNewListing
import os
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductTestCase(TestCase):   
    def setUp(self):
        self.productdetails = {
            'title': 'Blue Jeans',
            'price': 50,
            'description': 'Hole over left knee'}
        cur_path = os.path.dirname(__file__)
        new_path = os.path.join(cur_path, '..', 'media', 'resources', 'default.jpg')
        with open(new_path, 'rb') as file:
            self.image = SimpleUploadedFile(
                name='default.jpg',
                content=file.read(),
                content_type='image/jpeg'
            )
    def test_form(self):
        form = CreateNewListing(data=self.productdetails, files={'image': self.image})
        self.assertTrue(form.is_valid())
    def test_createListing(self):
        # send product data
        self.client.post('/createlisting/', data={**self.productdetails, 'image':self.image}, follow=True)
        # Check if the user is created in the database
        instances = Product.objects.all()
        print("\nPrinting all MyModel instances:")
        for instance in instances:
            print(instance)
        self.assertTrue(Product.objects.filter(name=self.productdetails['title']).exists())