from django.contrib import admin

from .models import Room, RoomPhoto, Gallery, About, Contacts, CategoryRoom, Reservation


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room
    # inlines = [AdminRoomPhoto]
    list_display = ["title", "inn_number", "position", "is_visible", "price", "special_offer"]
    list_editable = ["position", "is_visible", "price", "special_offer"]
    list_filter = ["is_visible", "special_offer", "category", "for_single", "with_pets", "first_floor"]


@admin.register(RoomPhoto)
class AdminAllRoomPhoto(admin.ModelAdmin):
    model = RoomPhoto
    list_filter = ["room"]
    list_display = ["room", "position"]
    list_editable = ["position"]


admin.site.register(Gallery)
admin.site.register(About)
admin.site.register(Contacts)
admin.site.register(CategoryRoom)

admin.site.register(Reservation)
