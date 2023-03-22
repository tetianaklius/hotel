from django.contrib import admin

from .models import Room, RoomPhoto, Gallery, About, Contacts, CategoryRoom, Reservation


class RoomPhotoAdmin(admin.TabularInline):
    model = RoomPhoto
    raw_id_fields = ["room"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Class that allows to manage and display in admin panel all instances of the category Room"""
    model = Room
    inlines = [RoomPhotoAdmin]
    list_display = ["inn_number", "title", "position", "is_visible", "price", "special_offer"]
    list_editable = ["position", "is_visible", "price", "special_offer"]
    list_filter = ["is_visible", "special_offer", "category", "for_single", "with_pets", "first_floor"]


@admin.register(RoomPhoto)
class AdminAllRoomPhoto(admin.ModelAdmin):
    """Class that allows to manage and display in admin panel all instances of the category RoomPhoto"""
    model = RoomPhoto
    list_filter = ["room"]
    list_display = ["room", "position"]
    list_editable = ["position"]


@admin.register(Gallery)
class AdminGallery(admin.ModelAdmin):
    """Class that allows to manage and display in admin panel all instances of the category Gallery"""
    model = Gallery
    list_filter = ["season", "is_visible"]
    list_display = ["inn_short_desc", "season", "is_visible"]
    list_editable = ["is_visible"]


admin.site.register(About)
admin.site.register(Contacts)


@admin.register(CategoryRoom)
class CategoryRoomAdmin(admin.ModelAdmin):
    """Class that allows to manage and display in admin panel all instances of the category CategoryRoom"""
    model = CategoryRoom
    list_display = ["title", "is_visible"]
    list_filter = ["is_visible"]


@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    """Class that allows to manage and display in admin panel all instances of the category Reservation"""
    model = Reservation
    list_display = ["name", "phone", "persons", "is_processed"]
    list_filter = ["persons", "is_processed", "date"]

