from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from main_page.forms import RoomReservationForm
from .models import RoomPhoto, Room, Reservation, Gallery, About, Contacts, CategoryRoom


def is_manager(user):
    return user.groups.filter(name="manager").exists()


def main(request):
    return render(request, "main_page.html", context={
        "gallery": list(Gallery.objects.filter(is_visible=True).order_by('?')[:8]),
        "about": About.objects.get(),
        "contacts": Contacts.objects.get(),

    })


def room_selection(request, category_persons=None):
    if category_persons:
        if category_persons==1:
            rooms_show = Room.objects.filter(is_visible=True, for_single=True)
            for item in rooms_show:
                if item.price_1person:
                    item.price = item.price_1person
                    item.price_comment = "(ціна за номер для проживання 1 особи)"

        elif category_persons==2:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
            for item in rooms_show:
                if item.price_2person:
                    item.price = item.price_2person
                    item.price_comment = "(ціна за номер для проживання 2-х осіб)"

        elif category_persons==3:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
            for item in rooms_show:
                if item.price_3person:
                    item.price = item.price_3person
                    item.price_comment = "(ціна за номер для проживання 3-х осіб)"

        elif category_persons==4:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)

        elif category_persons == 10:
            rooms_show = Room.objects.filter(is_visible=True, with_pets=True)
            for item in rooms_show:
                if item.price_pets:
                    item.price = item.price_pets
                    item.price_comment = "(ціна за номер для проживання з домашніми улюбленцями)"
        else:
            rooms_show = Room.objects.filter(is_visible=True)
    else:
        rooms_show = Room.objects.filter(is_visible=True)
    return render(request, "rooms.html", context={
        "rooms": rooms_show,
        "room_category": CategoryRoom.objects.filter(is_visible=True),
    })


def room_details(request, room_id: int):
    if room_id:
        room = Room.objects.filter(id=room_id).first()
        return render(request, "room_details.html", context={
            "room": room,
            "room_photos": RoomPhoto.objects.filter(room__id=room_id, room__is_visible=True).order_by("id"),
        })


def reservation(request, room_id):
    if request.user.is_authenticated:
        form = RoomReservationForm(initial={
            "name": request.user.first_name,
            "last_name": request.user.last_name,
            "room_id": room_id,
            "room_price": Room.objects.get(id=room_id).price,
            "persons": Room.objects.get(id=room_id).category.persons,
            "user_id": request.user.id,
            "user_email": request.user.email,
        })
    else:
        form = RoomReservationForm()
        form.room_id = room_id

    if form.is_valid():
        form.room_price = Room.objects.get(id=room_id).price
        form.user_id = request.user.id
        form.room_id = room_id
        form.save()
        return HttpResponseRedirect(reverse("main_page:main_path"))

    room = Room.objects.get(id=room_id)
    room_price = room.price

    return render(request, "reservation.html", context={
        "form": form,
        "room": room,
        "room_price": room_price,
        "room_id": room_id,
        "user_id": request.user.id or 2,
    })


# def reservation(request, room_id):
#     if request.method == "POST":
#         form = RoomReservationForm(request.POST)
#         form.room_id = room_id
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("main_page:main_path"))
#     else:
#         form = RoomReservationForm()
#         form.room_id = room_id
#         room = Room.objects.get(id=room_id)
#         return render(request, "reservation.html", context={
#             "form": form,
#             "room": room,
#         })


def filter_(request, category_id):
    rooms = Room.objects.filter(category_id)
    return render(request, "rooms.html", context={"rooms": rooms, })


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def update_reservation(request, pk):
    Reservation.objects.filter(pk=pk).update(is_processed=True)
    return redirect("main_page:list_reservations")


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def list_reservations(request):
    messages = Reservation.objects.filter(is_processed=False)
    for item in messages:
        room = Room.objects.get(id=item.room_id)
        room_price = room.price

    return render(request, "list_reservations.html", context={"reservations": messages, "room": room, "room_price": room_price, })

