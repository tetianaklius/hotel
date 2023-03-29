
from django.urls import path
from .views import logout_view, login_view, registration_view, profile_view, message_view

app_name = "account"

urlpatterns = [
    path("logout/", logout_view, name="logout_view"),
    path("login/", login_view, name="login_view"),
    path("registration/", registration_view, name="registration_view"),
    path("profile/", profile_view, name="profile"),
    path("message/", message_view, name="message_view"),

]