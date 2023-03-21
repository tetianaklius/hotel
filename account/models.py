from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# додаємо поле в User через  User.add_to_class

phone_validator = RegexValidator(regex=r'^\+?3?8?0\d{2}[- ]?(\d[- ]?){7}$', message='Error phone number')
phone = models.CharField(max_length=20, validators=[phone_validator], null=True, blank=True)

User.add_to_class('phone', models.CharField(max_length=20, blank=True, null=True))