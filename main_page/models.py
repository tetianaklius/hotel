from django.core.validators import RegexValidator
from django.db import models


def directory_path(instance, filename):
    """This function forms a file name so that files are stored in folders in an orderly manner"""
    return 'rooms_img/room_{0}/{1}'.format(instance.inn_number, filename)


def directory_path_img(instance, filename):
    """This function forms a file name so that files are stored in folders in an orderly manner"""
    return 'rooms_img/room_{0}/{1}'.format(instance.room.inn_number, filename)


class CategoryRoom(models.Model):
    """
    This class contains categories of rooms (rooms=instances of class Room) and are
    formed according to a certain principle (for example, by the quantity of persons). Categories are used in the filter
    and help to sort the rooms on the website page and make it easier for the user to choose.
    Each category has a title (title), position, quantity of persons (persons).
    """
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
    """
    This is the main subject on site. Instances of this class are rooms of hotel. They have their attributes such as
    title (title), description (desc), position on page (position), possible quantity of persons (persons).
    Pricing policy assumes that the price of a room may change depending on the quantity of people living in it and also
    on the presence or absence of pets. That is why different prices (price_1person, price_2person, price_3person,
    price_pets) are indicated, which the site administrator will adjust in admin panel.
    Field "special_offer" means whether the room is currently on special offer or not (this option will be used
    on site in future). Field "category" connects room with some category. Field "title_photo" contains the title photo
    of room. Field "inn_number" has an integer that is real number of the room in a hotel
    (it is not equal to the room id in admin panel). Fields "for_single", "with_pets", "first_floor"
    help to filter rooms according to the criteria can or can`t one person live in the room ("for_single"),
    is it possible to live in a room with pet(s) ("with_pets"), is the room on the first floor or isn`t ("first_floor").
    """
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
    title_photo = models.ImageField(upload_to=directory_path, blank=True, default='')

    inn_number = models.SmallIntegerField(blank=True, default=1)

    for_single = models.BooleanField(default=False)
    with_pets = models.BooleanField(default=False)
    first_floor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inn_number} | {self.title}"

    class Meta:
        ordering = ('position',)


class RoomPhoto(models.Model):
    """This class has instances with room photos, which are connected with rooms (rooms=instances of class Room)
    by ForeignKey and field "room" here. Instance of RoomPhoto has image file (photo), description (desc),
    position (position).
    """
    photo = models.ImageField(upload_to=directory_path_img)
    position = models.SmallIntegerField(unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_photo")
    desc = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return f"{self.photo.name}"

    class Meta:
        ordering = ("room", "position")


class Gallery(models.Model):
    """
    This class contains instances with general images for main page of the site, section Gallery.
    There are images (photo), their description (desc) for users, short description (inn_short_desc)
    for string presentation in admin panel, season of the year (season) for convenient filtering in admin panel.
    (Fields "title_site" and "subtitle_site" were created as fallbacks for the section heading and subheading
    (for manual control by the manager or administrator)).
    """
    # title_site = models.TextField(max_length=80, blank=True)
    # subtitle_site = models.TextField(max_length=250, blank=True)
    photo = models.ImageField(upload_to="gallery", blank=False)
    desc = models.TextField(max_length=250, blank=True)
    inn_short_desc = models.CharField(max_length=30, blank=False)
    season = models.SmallIntegerField()
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.inn_short_desc}"


class About(models.Model):
    """
    Instance of this class contains information about hotel for users of site. There are title of section (title),
    upper (sup_desc) and lower (inf_desc) description, also items with descriptive information about hotel
    (point_text 1-5). Also, there is an image (photo).
    """
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
    """
    There is a contact information to contact the hotel. There are title (title) and subtitle (sub_title) of section
    on main page, upper (sup_desc) and lower (inf_desc) description, fields for phone (phone),
    additional phone (phone_add), address (address), email (email) and additional email (email_add),
    field for information about pages in social networks (socials), some additional information (add_information),
    fields for open days and hours, days off. Also, some information fields have consonant fields with "_title" after,
    "_title" fields exist so that the site administrator can change the wording of the headings
    to present contact information.
    """
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
    """
    This class contains fields needed to send request of room reservation by the user and save this information
    (for future processing by manager). There is input information about user who want to reserve room
    (name, last name, phone, email), additional input text information from user (message),
    quantity of persons is needed, some internal information: room to be reserved (room), user id,
    date of request from user (date), date of processing by the manager (date_processing)
    and state of processing (is_processed: yes or not).
    """
    phone_validator = RegexValidator(regex=r"^\+?3?8?0\d{2}[- ]?(\d[- ]?){7}$", message="Помилка в номері телефону")

    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    user_email = models.CharField(max_length=100, blank=True, null=True)
    persons = models.IntegerField(null=True, blank=True, default=2)
    message = models.TextField(max_length=250, blank=True)

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room", default=1)
    room_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)

    date = models.DateField(auto_now_add=True)
    date_processing = models.DateField(auto_now=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {self.phone}"

    class Meta:
        ordering = ("-date",)
