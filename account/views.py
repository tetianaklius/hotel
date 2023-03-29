from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from main_page.models import About
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, AddUserProfileForm
from .models import UserProfile

User = get_user_model()


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
            new_user = form.save(commit=False)
            form.save()
            UserProfile.objects.create(user=new_user, phone=form.cleaned_data["phone"])
            return HttpResponseRedirect(reverse("account:login_view"))
    else:
        form = UserRegistrationForm()
    return render(request, "registration.html", context={"form": form})


def profile_view(request):
    """Method allow to render page with information of personal user account and update this information."""
    if request.method == "POST":  # update information of personal account
        user_form = UserProfileForm(data=request.POST, instance=request.user)  # user profile form \
        # connected with model User
        profile_form = AddUserProfileForm(instance=request.user.userprofile, data=request.POST)  # form with field \
        # "phone" connected with UserProfile class
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профіль успішно оновлено")
            return HttpResponseRedirect(reverse("account:profile"))
        else:
            messages.success(request, "Введіть номер телефону у форматі 099-999-99-99")
    else:
        user_form = UserProfileForm(instance=request.user)  # shows information of personal account
        profile_form = AddUserProfileForm(instance=request.user.userprofile)
    context = {"about": About.objects.first(),
               "user_form": user_form,
               "profile_form": profile_form,
               }
    return render(request, "profile.html", context)


def message_view(request):
    return render(request, "message.html", context={})
