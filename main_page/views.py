import tkinter

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# import tkinter
# import tkinter as tk
from tkinter import *

import telebot


from account.models import UserProfile
from main_page.forms import RoomReservationForm
from .models import RoomPhoto, Room, Reservation, Gallery, About, Contacts, CategoryRoom

User = get_user_model()
TOKEN = '5683712081:AAHOCCORZKYWHcnZ72U2nhnjK0h42HToBYY'


def is_manager(user):
    """
    This function checks if the user is a member of the group "manager".
    :param user: the user whose membership is being checked;
    :return: True or False.
    """
    return user.groups.filter(name="manager").exists()


def is_admin(user):
    """
    This function checks if the user is a member of the group "admin".
    :param user: the user whose membership is being checked;
    :return: True or False.
    """
    return user.groups.filter(name="admin").exists()


def main(request):
    """
    This function renders the main page of the site.
    :param request: WSGIRequest from path function in urlpatterns.
    :return: HttpResponse.
    """
    return render(request, "main_page.html", context={
        "gallery": list(Gallery.objects.filter(is_visible=True).order_by('?')[:8]),
        "about": About.objects.get(),
        "contacts": Contacts.objects.get(),

    })


def room_selection(request, category_persons: int = None):
    """
    This function helps user to filter rooms by category and implements the price policy of the rooms.
    :param request: WSGIRequest from path function in urlpatterns.
    :param category_persons: this is value of attribute "persons" of selected room category
        (room category is an instance of the class CategoryRoom).
    :return: render html page with filtered rooms with actual prices (according to price policy).
    """
    if category_persons:  # if some category is selected by user
        if category_persons == 1:
            rooms_show = Room.objects.filter(is_visible=True, for_single=True)  # filtered rooms by "for_single" value
            for item in rooms_show:
                if item.price_1person:  # if price for 1 person for this room is exist (is filled)
                    item.price = item.price_1person  # usual price of the room is replaced by price for 1 person
                    item.price_comment = "(ціна за номер для проживання 1 особи)"  # comment to the new price

        elif category_persons == 2:  # there will be filtered rooms with this or greater persons quantity
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
            for item in rooms_show:
                if item.price_2person:  # if price for 2 persons for this room is exist (is filled)
                    item.price = item.price_2person  # usual price of the room is replaced
                    item.price_comment = "(ціна за номер для проживання 2-х осіб)"  # comment to the new price

        elif category_persons == 3:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)
            for item in rooms_show:
                if item.price_3person:  # if price for 3 persons for this room is exist (is filled)
                    item.price = item.price_3person  # usual price of the room is replaced
                    item.price_comment = "(ціна за номер для проживання 3-х осіб)"  # comment to the new price

        elif category_persons == 4:
            rooms_show = Room.objects.filter(is_visible=True, persons__gte=category_persons)

        elif category_persons == 10:
            rooms_show = Room.objects.filter(is_visible=True, with_pets=True)  # filtered rooms by "with_pets" value
            for item in rooms_show:
                if item.price_pets:  # if price for living with pets for this room is exist (is filled)
                    item.price = item.price_pets  # usual price of the room is replaced
                    item.price_comment = "(ціна за номер для проживання з домашніми улюбленцями)"  # price comment
        else:
            rooms_show = Room.objects.filter(is_visible=True)
    else:  # if category is not selected by user
        rooms_show = Room.objects.filter(is_visible=True)  # there are all visible rooms of the hotel
    return render(request, "rooms.html", context={
        "rooms": rooms_show,
        "room_category": CategoryRoom.objects.filter(is_visible=True),
    })


def room_details(request, room_id: int):
    """
    This function render the page with detailed information of selected room (instance of class Room).
    :param request: WSGIRequest from path function in urlpatterns.
    :param room_id: id of selected room.
    :return: render html page (HttpResponse).
    """
    if room_id:
        room = Room.objects.filter(id=room_id).first()
        return render(request, "room_details.html", context={
            "room": room,
            "room_photos": RoomPhoto.objects.filter(room__id=room_id, room__is_visible=True).order_by("id"),
        })


def reservation(request, room_id: int):
    """
    This function works with form of room reservation and site page with this form,
    which allow user to fill and send request of room reservation.
    :param request: WSGIRequest from path function in urlpatterns.
    :param room_id: id of selected room to reserve.
    :return: render (HttpResponse).
    """
    user = request.user

    if request.method == "POST":
        form = RoomReservationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            room = Room.objects.get(id=room_id)  # extract the room object to have access to all its attributes
            room_number = room.inn_number
            # price depends on quantity of persons (according to price policy; look at room_selection function)
            if cd["persons"] == 1:
                room_price = room.price_1person
            elif cd["persons"] == 2:
                room_price = room.price_2person or room.price
            elif cd["persons"] == 3:
                room_price = room.price_3person or room.price
            else:
                room_price = room.price
            reservation_instance = Reservation(
                name=cd["name"],
                user_id=request.user.id,
                room_id=cd["room_id"],
                # room_number=room_number,
                message=cd["message"],
                phone=cd["phone"],
                persons=cd["persons"],
                room_price=room_price
            )
            reservation_instance.save()

            # informing the staff about the new reservation request
            bot = telebot.TeleBot(TOKEN)
            bot.send_message(
                "703984335",
                f'{cd["phone"]} | Бронювання: {cd["name"]}; {room_number} номер; {cd["persons"]} особ(и/а);'
                f' ціна {room_price} || «{cd["message"]}»'
            )

            ######################################################################################################
            # tkinter message window
            window = tkinter.Tk()
            #
            # # window geometry
            window_height = 250
            window_width = 450
            screen_width = window.winfo_screenwidth()  # gets the value of the width of the user`s screen
            screen_height = window.winfo_screenheight()  # gets the value of the height of the user`s screen
            x_coordinate = int((screen_width / 2) - (window_width / 2))
            y_coordinate = int((screen_height / 2) - (window_height / 2))
            window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

            window.resizable(False, False)  # to make the window with a fixed size
            window.attributes('-topmost', 1)  # to put window at the top of the stacking order

            def close_win():
                window.destroy()

            window.title("Садиба «Леонтія»")
            label = tkinter.Label(window, text="Вітаємо!\nЗаявку успішно надіслано!\n\n"
                                          "Невдовзі Вам зателефонує адміністратор", font=("Arial", 14), fg="#483D8B"
                             )
            label.pack(padx=20, pady=30)

            button = tkinter.Button(window, text="Гаразд", font=("Roboto", 12), foreground="#FFFFFF", command=close_win,
                               background="#483D8B"
                               )
            button.pack(pady=20)

            window.mainloop()

            # messagebox.showinfo("Бронювання", "Заявка надіслана успішно, невдовзі Вам зателефонує адміністратор")
            ######################################################################################################

            return HttpResponseRedirect(reverse("main_page:main_path"))

    else:
        room_price = Room.objects.get(id=room_id).price
        persons = Room.objects.get(id=room_id).category.persons

        name = user.first_name if user.is_authenticated else None
        last_name = user.last_name if user.is_authenticated else None
        user_id = request.user.id if user.is_authenticated else None
        user_email = request.user.email if user.is_authenticated else None

        user_profile = UserProfile.objects.filter(user=user).first() if user.is_authenticated else None
        user_phone = user_profile.phone if user_profile else None

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


@login_required(login_url="/login/")
@user_passes_test(is_manager)  # only user member of group "manager" has access
def update_reservation(request, pk: int):
    """
    This function allows the manager to update the reservation status (to "processed") after manual processing
    (phone talk with client, approval of details, booking confirmation).
    :param request: WSGIRequest from path function in urlpatterns.
    :param pk: pk of reservation (instance of class Reservation) to be updated.
    :return: redirect to the same page with list of all users unprocessed requests of reservations.
    """
    Reservation.objects.filter(pk=pk).update(is_processed=True)  # update status to "processed"
    return redirect("main_page:list_reservations")


@login_required(login_url="login/")
@user_passes_test(is_manager)  # only user member of group "manager" has access to this page
def list_reservations(request):
    """
    This function allow manager to have access to all users unprocessed requests of reservations on
    a separate page of the site.
    :param request: WSGIRequest from path function in urlpatterns.
    :return: render of page with list of all users unprocessed requests of reservations.
    """
    messages = Reservation.objects.filter(is_processed=False)  # users unprocessed requests of reservations

    return render(request, "list_reservations.html",
                  context={"reservations": messages, })
