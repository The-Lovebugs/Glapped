from django.test import TestCase
from .models import Product


class ProductTestCase(TestCase):   
    def setUp(self):
        self.productdetails = {
            'name': 'Blue Jeans',
            'price': 50,
            'description': 'Hole over left knee',
            'image': 'resources/default.jpg',
            'category': 'Clothes'}
    def test_createListing(self):
        # send product data
        response = self.client.post('/createlisting/', self.productdetails, follow=True)
        # Check if the user is created in the database
        self.assertTrue(Product.objects.filter(username=self.productdetails['name']).exists())