from django.urls import path
from .views import main, update_reservation, list_reservations, message

from .views import rooms, reservation, room_details

app_name = "main_page"

urlpatterns = [
    path("", main, name="main_path"),

    path("rooms/<int:persons>/", rooms, name="rooms"),

    path("rooms/room/reservation/<int:room_id> <int:persons>/", reservation, name="reservation"),
    path("reservation/message/", message, name="message"),

    path("rooms/room/<int:room_id> <int:persons>/", room_details, name="room_details"),

    path("manager/update_reserve/<int:pk>/", update_reservation, name="update_reservation"),
    path("manager/reserve_list/", list_reservations, name="list_reservations"),

]