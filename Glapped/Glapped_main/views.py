from django.shortcuts import render, get_object_or_404,HttpResponse, HttpResponseRedirect
from .models import Product, ListingReport
from .forms import CreateNewListing
from .forms import ReportForm
from django.contrib.auth.models import User
from register.models import UserProfile
# Create your views here.
def home(request):
    products = Product.objects.all().filter(reportAmount__lt=4)
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
    products = Product.objects.filter(name__icontains=query, reportAmount__lt=4) if query else []
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

def createReport(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST" :
        form = ReportForm(request.POST, request.FILES)
        #needs to not allows the same user to report the same product multiple times
        existingReports = ListingReport.objects.filter(reporter=request.user, product=product)
        if form.is_valid() and not existingReports.exists():
            reporter = request.user
            #listing = request.listing 
            category  = form.cleaned_data['reason']
            description = form.cleaned_data['description']
            ListingReport.objects.create(reporter=reporter,product=listing,category=category,description=description)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid form")
    else:
        form = ReportForm()
    return render(request, 'report.html', {"form": form})


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