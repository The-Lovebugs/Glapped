from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save the user object without committing to the database yet
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            # now save the user to the database
            user.save()

            # authenticate the user and log them in
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)

            # check if the user already has a profile; if not, create one
            userprofile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                # you can set default points here if you'd like (e.g. 0)
                userprofile.points = 0
                userprofile.save()

            return redirect('/')

    form = RegisterForm()
    return render(request, 'register/register.html', {"form": form})
