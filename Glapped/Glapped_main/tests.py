from django.test import TestCase
from .models import Product, BuyNowProduct, AuctionProduct
from .forms import CreateNewListing
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

#created to reduce clutter
def loginAndPost(self, userdetails, link, data):
    self.client.login(username=userdetails['username'], password=userdetails['password1'])
    return self.client.post(link, data, follow=True)

class buyNowProductTestCase(TestCase):
           
    def setUp(self):
        #instantiate product
        self.buynowproductdetails = {
            'title': 'Blue Jeans',
            'price': 50,
            'description': 'Hole over left knee',
            'category': 'jeans'
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
        self.client.post('/register/', data=self.userdetails)
        self.user = User.objects.get(username=self.userdetails['username'])
    
    def test_buyNowform_validData_isValid(self):
        form = CreateNewListing(data=self.buynowproductdetails, files={'image': self.image})
        self.assertTrue(form.is_valid())
        
    def test_buyNowform_emptyForm_isNotValid(self):
        form = CreateNewListing(data={}, files={'image': self.image})
        self.assertFalse(form.is_valid())
    
    def test_buyNowform_noPrice_isNotValid(self):
        self.buynowproductmissingdetails= {
            'title': 'Blue Jeans',
            'description': 'Hole over left knee',
            'category': 'jeans'
            }
        form = CreateNewListing(data=self.buynowproductmissingdetails, files={'image': self.image})
        self.assertFalse(form.is_valid())
        
    def test_buyNowform_negativePrice_isNotValid(self):
        self.buynowproductdetails['price'] = -1
        form = CreateNewListing(data=self.buynowproductdetails, files={'image': self.image})
        self.assertFalse(form.is_valid())
        
    def test_buyNowform_noImage_isNotValid(self):
        form = CreateNewListing(data=self.buynowproductdetails)
        self.assertFalse(form.is_valid())

    def test_createListing_validBuyNowData_productCreated(self):
        # send product data
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        # Check if the product is created in the database
        self.assertTrue(BuyNowProduct.objects.filter(name=self.buynowproductdetails['title']).exists())
        
    def test_createBuyNowListing_noData_errorMessage(self):
        # send product data
        response = loginAndPost(self, self.userdetails, '/createlisting/', data={})
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")
        
    
        
class buyNowBuyTestCase(TestCase):
           
    def setUp(self):
        #instantiate product
        self.buynowproductdetails = {
            'title': 'Blue Jeans',
            'price': 50,
            'description': 'Hole over left knee',
            'category': 'jeans'
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
        self.client.post('/register/', data=self.userdetails)
        self.user = User.objects.get(username=self.userdetails['username'])
        
        self.buyerdetails = {
            'username': 'testbuyer',
            'email': 'testbuyer@exeter.ac.uk',
            'password1': 'P455w0rd9?',
            'password2': 'P455w0rd9?'
            }
        self.client.post('/register/', data=self.buyerdetails)
        self.user2 = User.objects.get(username=self.buyerdetails['username'])
        
    def test_buy_buyNowProductBought_successMessage(self):
        #user1 creates listing
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        #user2 buys listing
        listing_pk = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).pk
        url = '/buy/' + str(listing_pk)
        response = loginAndPost(self, self.buyerdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #check that listing is bought
        message = list(response.context.get('messages'))[1]
        self.assertEqual(message.tags, "success")
    
    def test_buy_buyNowProductBought_buyerUpdates(self):
        #user1 creates listing
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        #user2 buys listing
        listing_pk = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).pk
        url = '/buy/' + str(listing_pk)
        loginAndPost(self, self.buyerdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #check that listing is sold
        isSold = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).sold
        self.assertTrue(isSold)
        
    def test_buy_buyNowProductBought_buyerUpdates(self):
        #user1 creates listing
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        #user2 buys listing
        listing_pk = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).pk
        url = '/buy/' + str(listing_pk)
        loginAndPost(self, self.buyerdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #check that listing is bought by user2
        buyer = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).buyer
        self.assertEqual(buyer,self.user2)
        
    def test_buy_buyerDoesntHaveEnoughPoints_errorMessage(self):
        #user1 creates listing
        self.buynowproductdetails['price'] = 200
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        #user2 buys listing
        listing_pk = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).pk
        url = '/buy/' + str(listing_pk)
        response = loginAndPost(self, self.buyerdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #check that error message given bought
        message = list(response.context.get('messages'))[1]
        self.assertEqual(message.tags, "error")
        
    def test_buy_buyerIsLister_errorMessage(self):
        #user1 creates listing
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        #user1 buys listing
        listing_pk = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).pk
        url = '/buy/' + str(listing_pk)
        response = loginAndPost(self, self.userdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #check that error message given bought
        message = list(response.context.get('messages'))[1]
        self.assertEqual(message.tags, "error")
        
    def test_buy_alreadyBought_errorMessage(self):
        #user1 creates listing
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.buynowproductdetails, 'image':self.image})
        #user2 uys listing
        listing_pk = BuyNowProduct.objects.get(name=self.buynowproductdetails['title']).pk
        url = '/buy/' + str(listing_pk)
        loginAndPost(self, self.buyerdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #attempt to purchase has already happened
        response = loginAndPost(self, self.buyerdetails, url, data={**self.buynowproductdetails, 'image':self.image})
        #check that error message given bought
        message = list(response.context.get('messages'))[2]
        self.assertEqual(message.tags, "error")


class auctionProductTestCase(TestCase):
    def setUp(self):
        #instantiate product
        self.auctionproductdetails = {
            'title': 'Blue Jeans',
            'starting_bid': 5,
            'auction_length': 3,
            'description': 'Hole over left knee',
            'category': 'jeans'
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
        self.client.post('/register/', data=self.userdetails)
        self.user = User.objects.get(username=self.userdetails['username'])
        
    def test_auctionform_validData_isValid(self):
        form = CreateNewListing(data=self.auctionproductdetails, files={'image': self.image})
        self.assertTrue(form.is_valid())
        
    def test_auctionform_emptyForm_isNotValid(self):
        form = CreateNewListing(data={}, files={'image': self.image})
        self.assertFalse(form.is_valid())
    
    def test_auctionform_noStartingBid_isNotValid(self):
        self.auctionproductmissingdetails = {
            'title': 'Blue Jeans',
            'auction_length': 3,
            'description': 'Hole over left knee',
            'category': 'jeans'
            }
        form = CreateNewListing(data=self.auctionproductmissingdetails, files={'image': self.image})
        self.assertFalse(form.is_valid())
        
    def test_auctionform_negativePrice_isNotValid(self):
        self.auctionproductdetails['starting_bid'] = -1
        form = CreateNewListing(data=self.auctionproductdetails, files={'image': self.image})
        self.assertFalse(form.is_valid())
        
    def test_auctionform_noImage_isNotValid(self):
        form = CreateNewListing(data=self.auctionproductdetails)
        self.assertFalse(form.is_valid())

    def test_createListing_validAuctionData_productCreated(self):
        # send product data
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.auctionproductdetails, 'image':self.image})
        # Check if the product is created in the database
        self.assertTrue(AuctionProduct.objects.filter(name=self.auctionproductdetails['title']).exists())


class functionsAuctionProductTestCase(TestCase):
    def setUp(self):
        #instantiate product
        self.auctionproductdetails = {
            'title': 'Blue Jeans',
            'starting_bid': 5,
            'auction_length': 3,
            'description': 'Hole over left knee',
            'category': 'jeans'
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
        self.client.post('/register/', data=self.userdetails)
        self.user = User.objects.get(username=self.userdetails['username'])
        
        self.buyerdetails = {
            'username': 'testbuyer',
            'email': 'testbuyer@exeter.ac.uk',
            'password1': 'P455w0rd9?',
            'password2': 'P455w0rd9?'
            }
        self.client.post('/register/', data=self.buyerdetails)
        self.user2 = User.objects.get(username=self.buyerdetails['username'])
        
    def test_auction_bidGreater_successMessage(self):
        #user1 creates listing
        loginAndPost(self, self.userdetails, '/createlisting/', data={**self.auctionproductdetails, 'image':self.image})
        #user2 buys listing
        listing_pk = AuctionProduct.objects.get(name=self.auctionproductdetails['title']).pk
        url = '/bid/' + str(listing_pk)
        response = loginAndPost(self, self.buyerdetails, url, data={'bid_amount':15})
        message = list(response.context.get('messages'))[1]
        print(str(message))
        self.assertEqual(message.tags, "success")