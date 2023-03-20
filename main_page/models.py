import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import get_object_or_404


class CategoryRoom(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    position = models.SmallIntegerField(unique=True)
    is_visible = models.BooleanField(default=True)
    persons = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ('position',)

    def __iter__(self):
        for item in self.rooms.all():
            yield item


class Room(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    desc = models.TextField(max_length=3000, blank=True)
    position = models.SmallIntegerField(unique=True)
    is_visible = models.BooleanField(default=True)
    persons = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_comment = models.TextField(max_length=100, blank=True)
    price_1person = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_2person = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_3person = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_pets = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    special_offer = models.BooleanField(default=False)
    category = models.ForeignKey(CategoryRoom, on_delete=models.CASCADE, related_name="rooms")
    title_photo = models.ImageField(upload_to="title_photo", blank=False)
    inn_number = models.SmallIntegerField(blank=True, default=1)

    for_single = models.BooleanField(default=False)
    with_pets = models.BooleanField(default=False)
    first_floor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inn_number} | {self.title}"

    class Meta:
        ordering = ('position',)


class RoomPhoto(models.Model):

    def get_file_name(self, file_name: str):
        ext = file_name.strip().split(".")[-1]
        file_name = f"{uuid.uuid4()}.{ext}"
        return os.path.join("room_photo", file_name)

    photo = models.ImageField(upload_to=get_file_name, blank=False)
    position = models.SmallIntegerField(unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_photo")
    desc = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.photo.name}"

    class Meta:
        ordering = ("room", "position")


class Gallery(models.Model):
    title_site = models.TextField(max_length=80, blank=True)
    subtitle_site = models.TextField(max_length=250, blank=True)
    photo = models.ImageField(upload_to="gallery", blank=False)
    desc = models.TextField(max_length=250, blank=True)
    inn_short_desc = models.CharField(max_length=30, blank=False)
    season = models.SmallIntegerField()
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.inn_short_desc}"


class About(models.Model):
    title = models.CharField(max_length=100, blank=True)
    sup_desc = models.TextField(max_length=2000, blank=True)
    point_text_1 = models.TextField(max_length=200, blank=False)
    point_text_2 = models.TextField(max_length=200, blank=False)
    point_text_3 = models.TextField(max_length=200, blank=False)
    point_text_4 = models.TextField(max_length=200, blank=True)
    point_text_5 = models.TextField(max_length=200, blank=True)
    inf_desc = models.TextField(max_length=2000, blank=True)
    is_visible = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="about", blank=False)

    def __str__(self):
        return "About"


class Contacts(models.Model):
    title = models.TextField(max_length=100, blank=True)
    sub_title = models.TextField(max_length=500, blank=True)

    phone_title = models.TextField(max_length=20, blank=True)
    phone = models.TextField(max_length=20, blank=False)
    phone_add = models.TextField(max_length=20, blank=True)
    address_title = models.TextField(max_length=50, blank=True)
    address = models.TextField(max_length=200, blank=False)
    email_title = models.TextField(max_length=10, blank=True)
    email = models.TextField(max_length=50, blank=True)
    email_add = models.TextField(max_length=50, blank=True)
    socials = models.TextField(max_length=100, blank=True)

    add_information = models.TextField(max_length=500, blank=True)

    open_hours_title = models.TextField(max_length=20, blank=True)
    open_days_1 = models.TextField(max_length=150, blank=False)
    open_hours_1 = models.TextField(max_length=50, blank=False)
    open_days_2 = models.TextField(max_length=150, blank=True)
    open_hours_2 = models.TextField(max_length=50, blank=True)

    day_off_title = models.TextField(max_length=15, blank=True)
    day_off = models.TextField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.title}'


class Reservation(models.Model):
    phone_validator = RegexValidator(regex=r"^\+?3?8?0\d{2}[- ]?(\d[- ]?){7}$", message="Помилка в номері телефону")

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    persons = models.IntegerField(blank=True, default=2)
    message = models.TextField(max_length=250, blank=True)

    room_id = models.IntegerField()
    room_price = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    user_id = models.IntegerField(default=2, blank=True)
    # user_email = models.CharField(max_length=100, blank=True)

    date = models.DateField(auto_now_add=True)
    date_processing = models.DateField(auto_now=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.phone}"

    class Meta:
        ordering = ("-date", )
