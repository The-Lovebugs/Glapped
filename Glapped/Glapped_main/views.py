from django.shortcuts import render, get_object_or_404,HttpResponseRedirect, get_object_or_404, redirect,HttpResponse
from http.client import HTTPResponse
from .models import Product, BuyNowProduct, AuctionProduct, ListingReport
from .forms import CreateNewListing
from .forms import ReportForm
from django.contrib.auth.models import User
from register.models import UserProfile

from glapchat.models import Room
# Create your views here.
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.handlers.wsgi import WSGIRequest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from itertools import chain
from django.db.models import Q
import random

from .models import CATEGORY_SAVINGS



def home(request:WSGIRequest) -> HttpResponse:
    '''
    Function to render the generic home page, loads all
    products from the database.
    '''
    
    # Only show unsold buy now products
    buy_now_products = BuyNowProduct.objects.filter(
        sold=False,
        reportAmount__lt=4
        )
    
    # Only show active auctions
    auction_products = AuctionProduct.objects.filter(
        end_time__gt=timezone.now(),
        reportAmount__lt=4
        ) 

    # Combine both to display on homepage
    products = list(buy_now_products) + list(auction_products)  
    random.shuffle(products)

    return render(
        request,
        "home.html",
        {"products": products}
        )


def product_page(request:WSGIRequest, pk) -> HttpResponse:
    '''
    Function to render an individual product page.
    Loads data via a product key
    '''
    product = BuyNowProduct.objects.filter(pk=pk).first()

    if not product:
        product = AuctionProduct.objects.filter(pk=pk).first()

     # Show the 404 page if the product can't be found
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
    query = request.GET.get('q', '').strip()

    if query:
        # Search for name, description, and category, and less than 4 reports
        buy_now_products = BuyNowProduct.objects.filter(
            Q(sold=False),
            Q(reportAmount__lt=4),
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

        auction_products = AuctionProduct.objects.filter(
            Q(end_time__gt=timezone.now()),
            Q(reportAmount__lt=4),
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

        # Combine results and randomize
        products = list(buy_now_products) + list(auction_products)
        random.shuffle(products)

    else:
        products = []  # No query, return nothing

    return render(request, 'search.html', {'products': products, 'query': query})


def createListing(request):
    '''
    Method to generate a new listing from user input
    '''
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

            # Process and resize the image if it exists
            if image:
                try:
                    # Open the uploaded image
                    img = Image.open(image)
                    
                    # Set maximum dimensions (adjust as needed)
                    max_width = 500
                    max_height = 600
                    
                    # Resize if necessary while maintaining aspect ratio
                    if img.width > max_width or img.height > max_height:
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                        
                        # Convert to BytesIO buffer
                        output = BytesIO()
                        
                        # Save resized image (adjust format as needed)
                        if img.format == 'JPEG':
                            img.save(output, format='JPEG', quality=85)
                        elif img.format == 'PNG':
                            img.save(output, format='PNG', optimize=True)
                        else:
                            img.save(output, format='JPEG', quality=85)
                            
                        output.seek(0)
                        
                        # Create a new InMemoryUploadedFile
                        image = InMemoryUploadedFile(
                            output,
                            'ImageField',
                            f"{image.name.split('.')[0]}_resized.{img.format.lower()}",
                            f'image/{img.format.lower()}',
                            output.tell(),
                            None
                        )
                except Exception as e:
                    messages.error(request, f"Error processing image: {str(e)}")
                    return redirect('createListing')

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

def createReport(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST" :
        form = ReportForm(request.POST, request.FILES)
        #needs to not allows the same user to report the same product multiple times
        existingReport = ListingReport.objects.filter(reporter=request.user, product=product)
        if form.is_valid() and not existingReport.exists():
            reporter = request.user
            category  = form.cleaned_data['reason']
            description = form.cleaned_data['description']
            ListingReport.objects.create(reporter=reporter,product=product,category=category,description=description)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid form")
    else:
        form = ReportForm()
    return render(request, 'report.html', {"form": form, "pk":pk})

def leaderBoard(request:WSGIRequest) -> HttpResponse:
    '''
    Render the leaderboard webpage
    '''
    users_co2 = UserProfile.objects.order_by('-co2_saved')[:10]  # Top 10 for CO2
    users_water = UserProfile.objects.order_by('-water_saved')[:10]  # Top 10 for water
    return render(request, 'leaderBoard.html', {"users_co2": users_co2, "users_water": users_water})


def buy(request:WSGIRequest, pk: int) -> HttpResponseRedirect:
    '''
    Handles the purchase of a BuyNowProduct
    '''
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

    product.user.userprofile.save()
    request.user.userprofile.save()

    product.save()

    messages.success(request, "Purchase successful!")  # Success message after purchase
    return HttpResponseRedirect("/")  # Redirect to homepage


def message(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    if request.user == Product.objects.get(pk=pk).user:
        return HTTPResponse("You can't message yourself!")
    product = Product.objects.get(pk=pk)
    existing_room = Room.objects.filter(user=request.user, seller=product.user, product=product).first()
    if existing_room:
        return HttpResponseRedirect("/glapchat/" + str(existing_room.ID))
    room = Room.objects.create(user=request.user, seller=Product.objects.get(pk=pk).user, product=Product.objects.get(pk=pk))
    return HttpResponseRedirect("/glapchat/" + str(room.ID))
    


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



def custom_404(request:WSGIRequest, exception) -> HttpResponse:
    '''
    error page
    '''
    return render(request, '404.html', status=404)
