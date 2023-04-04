from django.urls import path
from .views import main, update_reservation, list_reservations, message

from .views import room_selection, reservation, room_details

app_name = "main_page"

urlpatterns = [
    path("", main, name="main_path"),

    path("rooms/", room_selection, name="room_selection"),
    path("rooms/category/<int:quantity_person>/", room_selection, name="category"),

    path("rooms/room/reservation/<int:room_id> <int:persons>/", reservation, name="reservation"),
    path("reservation/message/", message, name="message"),

    path("rooms/room/<int:room_id> <int: quantity_person>/", room_details, name="room_details"),

    path("manager/update_reserve/<int:pk>/", update_reservation, name="update_reservation"),
    path("manager/reserve_list/", list_reservations, name="list_reservations"),

]