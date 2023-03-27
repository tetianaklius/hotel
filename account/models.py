from django.contrib.auth import get_user_model
from django.db import models

from django.core.validators import RegexValidator

User = get_user_model()

phone_validator = RegexValidator(regex=r'^\+?3?8?0\d{2}[- ]?(\d[- ]?){7}$', message='Error phone number')


class UserProfile(models.Model):
    """This class allow to add a phone field in a one to one connection with user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, validators=[phone_validator], null=True, blank=True)

    def __str__(self):
        return "Профіль {}".format(self.user.username)
