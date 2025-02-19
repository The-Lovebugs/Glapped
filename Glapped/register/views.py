from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():    
            form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            form.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user = User.objects.get(username=username)
            userprofile = UserProfile.objects.create(user=user)
            userprofile.save()

            return redirect('/')
    
    form = RegisterForm()
    return render(request, 'register/register.html', {"form": form})