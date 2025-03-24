from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .models import Product, BuyNowProduct, AuctionProduct
from .forms import CreateNewListing
from django.contrib.auth.models import User
from register.models import UserProfile
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from itertools import chain
import random

from .models import CATEGORY_SAVINGS


def home(request):
    buy_now_products = BuyNowProduct.objects.filter(sold=False)  # Only show unsold buy now products
    auction_products = AuctionProduct.objects.filter(end_time__gt=timezone.now())  # Only show active auctions

    products = list(buy_now_products) + list(auction_products)  # Combine both to display on homepage
    random.shuffle(products)

    return render(request, "home.html", {"products": products})


def product_page(request, pk):
    product = BuyNowProduct.objects.filter(pk=pk).first()

    if not product:
        product = AuctionProduct.objects.filter(pk=pk).first()

    if not product:
        return render(request, '404.html', status=404) # Show the custom 404 page

    return render(request, 'listing.html', {'product': product, 'now': timezone.now()})


def account(request):
    user = User.objects.get(username=request.user)


    # Active Products (unsold BuyNow and ongoing Auctions)
    active_buy_now = BuyNowProduct.objects.filter(user=user, sold=False)
    active_auctions = AuctionProduct.objects.filter(user=user, end_time__gt=timezone.now(), sold=False)
    active_products = list(chain(active_buy_now, active_auctions))

    # Sold Products (completed BuyNow and Auctions sold)
    sold_buy_now = BuyNowProduct.objects.filter(user=user, sold=True)
    sold_auctions = AuctionProduct.objects.filter(user=user, sold=True)
    sold_products = list(chain(sold_buy_now, sold_auctions))

    # Bought/Won Products (Bought via BuyNow, or Won via Auction)
    bought_products = BuyNowProduct.objects.filter(buyer=user)
    won_auctions = AuctionProduct.objects.filter(winner=user, sold=True)
    bought_won_products = list(chain(bought_products, won_auctions))

    return render(request, 'account.html', {"activeProducts": active_products, "boughtProducts": bought_products, "soldProducts": sold_products})


def search(request):
    query = request.GET.get('q', '')
    products = BuyNowProduct.objects.filter(name__icontains=query) if query else []
    return render(request, 'search.html', {'products': products, 'query': query})


def createListing(request):
    if request.method == "POST":
        form = CreateNewListing(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data.get("price")
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            starting_bid = form.cleaned_data.get("starting_bid")
            auction_length = form.cleaned_data.get("auction_length")
            user = request.user

            # Handle Buy Now products
            if price:
                starting_bid = None  # Ensure no auction-related fields for Buy Now
                auction_length = None

                BuyNowProduct.objects.create(
                    name=title,
                    description=description,
                    category=category,
                    image=image,
                    price=price,
                    user=user,
                    sold=False,
                    buyer=None
                )

            # Handle Auction products
            elif starting_bid:
                price = None
                try:
                    auction_length = int(auction_length)  # Convert to integer
                except (ValueError, TypeError):
                    messages.error(request, "Invalid auction length. Please enter a valid number of days.")
                    return redirect('createListing')

                # Set the start and end times
                start_time = timezone.now()
                end_time = start_time + timedelta(days=auction_length)

                # Create AuctionProduct with auction_length
                AuctionProduct.objects.create(
                    name=title,
                    description=description,
                    category=category,
                    image=image,
                    starting_bid=starting_bid,
                    current_highest_bid=None,
                    start_time=start_time,
                    end_time=end_time,
                    user=user,
                    auction_length=auction_length
                )

            messages.success(request, "Listing created successfully!")
            return HttpResponseRedirect("/")  # Redirect to homepage

        else:
            messages.error(request, "Invalid form submission.")
            return redirect('createListing')

    else:
        form = CreateNewListing()

    return render(request, 'createListing.html', {"form": form})


def leaderBoard(request):
    users_co2 = UserProfile.objects.order_by('-co2_saved')[:10]  # Top 10 for CO2
    users_water = UserProfile.objects.order_by('-water_saved')[:10]  # Top 10 for water
    return render(request, 'leaderBoard.html', {"users_co2": users_co2, "users_water": users_water})




def buy(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    product = BuyNowProduct.objects.get(pk=pk)

    if request.user == product.user:
        messages.error(request, "You can't buy your own product!")
        return redirect("product_page", pk=product.pk)

    if product.sold:
        messages.error(request, "This product has already been sold!")
        return redirect("product_page", pk=product.pk)

    if request.user.userprofile.points < product.price:
        messages.error(request, "You don't have enough points to buy this product!")
        return redirect("product_page", pk=product.pk)

    request.user.userprofile.points -= product.price  # Deduct points from buyer

    product.user.userprofile.points += product.price  # Reward points to seller

    product.sold = True
    product.buyer = request.user

    # Update water and CO2 savings
    savings = CATEGORY_SAVINGS.get(product.category, CATEGORY_SAVINGS['misc'])
    request.user.userprofile.water_saved += savings['water']
    request.user.userprofile.co2_saved += savings['co2']


    product.user.userprofile.save()
    request.user.userprofile.save()

    product.save()

    messages.success(request, f"Purchase successful! You saved {savings['water']} litres of water and {savings['co2']} kg of CO₂!")  # Success message after purchase
    return HttpResponseRedirect("/")  # Redirect to homepage


def place_bid(request, pk):
    auction = get_object_or_404(AuctionProduct, id=pk)

    # Prevent bidding on own auction
    if request.user == auction.user:
        messages.error(request, "You cannot bid on your own listing!")
        return redirect("product_page", pk=auction.id)

    # Ensure auction is still active
    if auction.end_time < timezone.now():
        messages.error(request, "This auction has already ended!")
        return redirect("product_page", pk=auction.id)

    bid_amount = request.POST.get("bid_amount")

    try:
        bid_amount = int(bid_amount)

        # Check if user has enough available points
        user_profile = request.user.userprofile
        if bid_amount > user_profile.points:
            messages.error(request, "You do not have enough points to place this bid!")
            return redirect("product_page", pk=auction.id)

        # Ensure bid is higher than current highest bid or starting bid
        if bid_amount <= (auction.current_highest_bid or auction.starting_bid):
            messages.error(request, "Your bid must be higher than the current highest bid!")
            return redirect("product_page", pk=auction.id)

        # Deduct bid amount from available points
        user_profile.points -= bid_amount
        user_profile.save()

        # Refund previous highest bidder (if there was one)
        if auction.current_highest_bidder:
            auction.current_highest_bidder.userprofile.points += auction.current_highest_bid
            auction.current_highest_bidder.userprofile.save()

        # Update auction with new highest bid and bidder
        auction.current_highest_bid = bid_amount
        auction.current_highest_bidder = request.user
        auction.save()

        messages.success(request, "Your bid was successfully placed!")

    except (ValueError, TypeError):
        messages.error(request, "Invalid bid amount. Please enter a valid number.")

    return redirect("product_page", pk=auction.id)



def custom_404(request, exception):
    return render(request, '404.html', status=404)
