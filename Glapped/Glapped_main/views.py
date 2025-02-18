from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Product
from .forms import CreateNewListing
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})

def createListing(request):
    if request.method == "POST":
        form = CreateNewListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            Product.objects.create(name=title, description=description, price=price)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Invalid form")
    else:
        form = CreateNewListing()

    return render(request, 'createListing.html', {"form": form})