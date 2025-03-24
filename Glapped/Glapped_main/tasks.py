# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import AuctionProduct

@shared_task
def end_expired_auctions():
    auctions = AuctionProduct.objects.filter(end_time__lte=timezone.now(), sold=False)

    for auction in auctions:
        auction.end_auction()  # Ends auctions that have elapsed their time
