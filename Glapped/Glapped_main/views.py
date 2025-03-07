from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Product
from .forms import CreateNewListing
from django.contrib.auth.models import User
from register.models import UserProfile

from glapchat.models import Room
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def product_page(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'listing.html', {'product': product})

def account(request):
    user = User.objects.get(username=request.user)
    products = Product.objects.filter(user=user)
    activeProducts = products.filter(sold=False)
    soldProducts = products.filter(sold=True)
    boughtProducts = Product.objects.filter(buyer=user)

    return render(request, 'account.html', {"products": products, "activeProducts": activeProducts, "boughtProducts": boughtProducts, "soldProducts": soldProducts})

def search(request):
    query = request.GET.get('q','')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'search.html', {'products': products, 'query': query})

def createListing(request):
    if request.method == "POST":
        form = CreateNewListing(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            user = request.user
            Product.objects.create(name=title, description=description, price=price, image=image, category=category, user=user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid form")
    else:
        form = CreateNewListing()

    return render(request, 'createListing.html', {"form": form})


def leaderBoard(request):
    users = User.objects.all()
    userProfiles = UserProfile.objects.all().order_by('points').reverse()
    return render(request, 'leaderBoard.html', {"users": userProfiles})

def buy(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    
    product = Product.objects.get(pk=pk)

    if request.user == product.user:
        return HttpResponse("You can't buy your own product!")
    if product.sold:
        return HttpResponse("This product has already been sold!")
    if request.user.userprofile.points < Product.objects.get(pk=pk).price:
        return HttpResponse("You don't have enough points to buy this product!")
    

    request.user.userprofile.points -= product.price #deduct points from buyer

    product.user.userprofile.points += product.price #reward points to seller

    product.sold = True
    product.buyer = request.user

    product.user.userprofile.save()
    request.user.userprofile.save()

    product.save()

    return HttpResponseRedirect("/")


def message(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    if request.user == Product.objects.get(pk=pk).user:
        return HttpResponse("You can't message yourself!")
    product = Product.objects.get(pk=pk)
    existing_room = Room.objects.filter(user=request.user, seller=product.user, product=product).first()
    if existing_room:
        return HttpResponseRedirect("/glapchat/" + str(existing_room.ID))
    room = Room.objects.create(user=request.user, seller=Product.objects.get(pk=pk).user, product=Product.objects.get(pk=pk))
    return HttpResponseRedirect("/glapchat/" + str(room.ID))