from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from main_page.forms import RoomReservationForm
from .models import RoomPhoto, Room, Reservation, Gallery, About, Contacts, CategoryRoom


def category_coefficient(category_id):
    category = CategoryRoom.objects.get(id=category_id)
    return category.category_coefficient


def is_manager(user):
    return user.groups.filter(name="manager").exists()


def main(request):
    return render(request, "main_page.html", context={
        "gallery": Gallery.objects.all(),
        "about": About.objects.get(),
        "contacts": Contacts.objects.get(),

    })


def room_selection(request, category_persons=None):
    if category_persons:
        if category_persons==1:
            rooms_show = Room.objects.filter(is_visible=True, for_single=True)
            for item in list(rooms_show):
                if item.category.price_modification:
                    coefficient = category_coefficient(item.category.id)
                    item.price *= coefficient
        elif category_persons == 10:
            rooms_show = Room.objects.filter(is_visible=True, with_pets=True)
            for item in rooms_show:
                if item.category.price_modification:
                    coefficient = category_coefficient(item.category.id)
                    item.price *= coefficient
        else:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
    else:
        rooms_show = Room.objects.filter(is_visible=True)
    return render(request, "rooms.html", context={
        "rooms": rooms_show,
        "room_photos": RoomPhoto.objects.all(),
        "room_category": CategoryRoom.objects.all(),
    })


def room_details(request, room_id: int):
    if room_id:
        room = Room.objects.filter(id=room_id).first()
        return render(request, "room_details.html", context={
            "room": room,
            "room_photos": RoomPhoto.objects.filter(room__id=room_id, room__is_visible=True).order_by("id"),
        })


def reservation(request, room_id):
    if request.method == "POST":
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("main_page:main_path"))
    else:
        form = RoomReservationForm()
    return render(request, "reservation.html", context={
            "form": form,
            "room_id": room_id,
        })


def filter_(request, category_id):
    rooms = Room.objects.filter(category_id)
    return render(request, "rooms.html", context={"rooms": rooms,})


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def update_reservation(request, pk):
    Reservation.objects.filter(pk=pk).update(is_processed=True)
    return redirect("main_page:list_reservations")


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def list_reservations(request):
    messages = Reservation.objects.filter(is_processed=False)
    return render(request, "reservation.html", context={"reservations": messages})

