from django.contrib import admin
from .models import Product, BuyNowProduct, AuctionProduct, ListingReport
# Register your models here.


admin.site.register(Product)
admin.site.register(BuyNowProduct)
admin.site.register(AuctionProduct)
admin.site.register(ListingReport)