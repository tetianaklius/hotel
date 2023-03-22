from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse
from main_page.models import About


def login_view(request):
    """Method allow to enter to personal account on site."""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
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
    """Method allow to go out of personal account on site."""
    auth.logout(request)
    return redirect("/")


def registration_view(request):
    """Method allow to create personal user account on site."""
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("account:login_view"))
    else:
        form = UserRegistrationForm()
    return render(request, "registration.html", context={"form": form})


def profile_view(request):
    """Method allow to render page with information of personal user account on site."""
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("account:profile"))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {"form": form, "about": About.objects.first()}
    return render(request, "profile.html", context)



