from django.test import TestCase
from .models import Product
from .forms import CreateNewListing
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


class ProductTestCase(TestCase):   
    def setUp(self):
        #instantiate product
        self.productdetails = {
            'title': 'Blue Jeans',
            'price': 50,
            'description': 'Hole over left knee',
            'category': 'jeans',
            }
        #image for form entry
        cur_path = os.path.dirname(__file__)
        new_path = os.path.join(cur_path, '..', 'media', 'resources', 'default.jpg')
        with open(new_path, 'rb') as file:
            self.image = SimpleUploadedFile(
                name='default.jpg',
                content=file.read(),
                content_type='image/jpeg'
            )
        #user for form entry
        self.userdetails = {
            'username': 'testseller',
            'email': 'testuser@exeter.ac.uk',
            'password1': 'P455w0rd9!',
            'password2': 'P455w0rd9!'
            }
        self.client.post('/register/', data=self.userdetails, follow=True)
        self.user = User.objects.get(username=self.userdetails['username'])
    def test_form(self):
        form = CreateNewListing(data=self.productdetails, files={'image': self.image})
        print(form.errors)
        self.assertTrue(form.is_valid())
    def test_createListing(self):
        # send product data
        self.client.post('/createlisting/', data={**self.productdetails, 'image':self.image, 'user':self.user}, follow=True)
        # Check if the user is created in the database
        instances = Product.objects.all()
        print("\nPrinting all MyModel instances:")
        for instance in instances:
            print(instance)
        self.assertTrue(Product.objects.filter(name=self.productdetails['title']).exists())