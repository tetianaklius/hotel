from django.contrib.auth import login
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from main_page.models import About
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def login_view(request):
    """Method allow user to log in to personal account on site."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)  # form for login
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("main_page:main_path"))
    else:
        form = UserLoginForm()
    context = {"form": form}
    return render(request, "login.html", context)


def logout_view(request):
    """Method allow user to log out of personal account on site."""
    auth.logout(request)
    return redirect("/")


def registration_view(request):
    """Method allow user to create personal user account (registrate) on site."""
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)  # form for registration
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("account:login_view"))
    else:
        form = UserRegistrationForm()
    return render(request, "registration.html", context={"form": form})


def profile_view(request):
    """Method allow to render page with information of personal user account and update this information."""
    if request.method == "POST":  # update information of personal account
        form = UserProfileForm(data=request.POST, instance=request.user)  # user profile form connected with model User
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("account:profile"))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)  # show information of personal account
    context = {"form": form, "about": About.objects.first()}
    return render(request, "profile.html", context)



