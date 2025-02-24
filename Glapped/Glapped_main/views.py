from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Product
from .forms import CreateNewListing
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def product_page(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'listing.html', {'product': product})

def account(request):
    return render(request, 'account.html')

def createListing(request):
    if request.method == "POST":
        form = CreateNewListing(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            
            Product.objects.create(name=title, description=description, price=price, image=image, category=category)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid form")
    else:
        form = CreateNewListing()

    return render(request, 'createListing.html', {"form": form})