from django.contrib import admin
from django.contrib.auth.models import User

from account.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Class that allows to manage and display in admin panel all instances of the category Room"""
    model = UserProfile
