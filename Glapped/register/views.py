from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            form.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    
    form = RegisterForm()
    return render(request, 'register/register.html', {"form": form})