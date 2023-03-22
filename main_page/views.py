from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import url
from django.urls import reverse

from main_page.forms import RoomReservationForm
from .models import RoomPhoto, Room, Reservation, Gallery, About, Contacts, CategoryRoom


def is_manager(user):
    return user.groups.filter(name="manager").exists()


def is_admin(user):
    return user.groups.filter(name="admin").exists()


def main(request):
    return render(request, "main_page.html", context={
        "gallery": list(Gallery.objects.filter(is_visible=True).order_by('?')[:8]),
        "about": About.objects.get(),
        "contacts": Contacts.objects.get(),

    })


def room_selection(request, category_persons=None):
    if category_persons:
        if category_persons == 1:
            rooms_show = Room.objects.filter(is_visible=True, for_single=True)
            for item in rooms_show:
                if item.price_1person:
                    item.price = item.price_1person
                    item.price_comment = "(ціна за номер для проживання 1 особи)"

        elif category_persons == 2:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
            for item in rooms_show:
                if item.price_2person:
                    item.price = item.price_2person
                    item.price_comment = "(ціна за номер для проживання 2-х осіб)"

        elif category_persons == 3:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
            for item in rooms_show:
                if item.price_3person:
                    item.price = item.price_3person
                    item.price_comment = "(ціна за номер для проживання 3-х осіб)"

        elif category_persons == 4:
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
    user = request.user

    if request.method == "POST":
        form = RoomReservationForm(data=request.POST)
        if form.is_valid():
            reservation_instance = Reservation(
                name=form.cleaned_data["name"],
                user_id=request.user.id,
                room_id=form.cleaned_data["room_id"],
                message=form.cleaned_data["message"],
                phone=form.cleaned_data["phone"],
                persons=form.cleaned_data["persons"],
                room_price=Room.objects.get(id=room_id).price
            )
            reservation_instance.save()
            return HttpResponseRedirect(reverse("main_page:main_path"))

    else:
        room_price = Room.objects.get(id=room_id).price
        persons = Room.objects.get(id=room_id).category.persons

        name = user.first_name if user.is_authenticated else None
        last_name = user.last_name if user.is_authenticated else None
        user_id = request.user.id if user.is_authenticated else None
        user_email = request.user.email if user.is_authenticated else None
        user_phone = request.user.phone if user.is_authenticated else None

        form = RoomReservationForm(initial={
            'room_id': room_id,
            'room_price': room_price,
            'persons': persons,
            'name': name,
            'last_name': last_name,
            'user_id': user_id,
            'user_email': user_email,
            'phone': user_phone,
        })

    room = Room.objects.get(id=room_id)

    return render(request, "reservation.html", context={
        "form": form,
        "room": room,
    })


def filter_(request, category_id):
    rooms = Room.objects.filter(category_id)
    return render(request, "rooms.html", context={"rooms": rooms, })


@login_required(login_url="/login/")
@user_passes_test(is_manager)
def update_reservation(request, pk):
    Reservation.objects.filter(pk=pk).update(is_processed=True)
    return redirect("main_page:list_reservations")


@login_required(login_url="login/")
@user_passes_test(is_manager)
def list_reservations(request):
    messages = Reservation.objects.filter(is_processed=False)

    return render(request, "list_reservations.html",
                  context={"reservations": messages, })

