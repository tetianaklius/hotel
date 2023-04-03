import telebot


# the logic of the room price policy and the function of informing the staff are written here

def message_telegram(reservation):
    # informing the staff about the new reservation request
    TOKEN = '5683712081:AAHOCCORZKYWHcnZ72U2nhnjK0h42HToBYY'
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(
        "703984335",
        f'{reservation.phone} | Бронювання: {reservation.name} {reservation.room.inn_number} '
        f'номер; {reservation.persons} особ(и/а);'
        f' ціна {reservation.room_price} || «{reservation.message}»'
    )


def rooms_actual_price(persons: int, rooms):
    """
    This function filters rooms to show depending on the needed number of guests (persons) or some other values
    (look at inline comments below). Also, this function determines the price of the room (among available class
    variables) according to the condition (if such a price exist (is filled by site administrator)).
    :param persons: the needed number of guests.
    :param rooms: one or few objects (instances) of the Room class.
    :return: filtered rooms objects (with defined prices).
    """
    if persons == 1:
        rooms_show = rooms.filter(for_single=True)  # filtered rooms by "for_single" value
        for item in rooms_show:
            if item.price_1person:  # if price for 1 person for this room exists (is filled)
                item.price = item.price_1person  # usual price of the room is replaced by price for 1 person
            item.price_comment = "(ціна за номер для проживання 1 особи)"  # comment to the price

    elif persons == 2:  # there will be filtered rooms with this or greater persons quantity
        rooms_show = rooms.filter(persons__gte=persons)
        for item in rooms_show:
            if item.price_2person:  # if price for 2 persons for this room exists (is filled)
                item.price = item.price_2person  # usual price of the room is replaced
            item.price_comment = "(ціна за номер для проживання 2-х осіб)"  # comment to the price

    elif persons == 3:
        rooms_show = rooms.filter(persons__gte=persons)
        for item in rooms_show:
            if item.price_3person:  # if price for 3 persons for this room exists (is filled)
                item.price = item.price_3person  # usual price of the room is replaced
            item.price_comment = "(ціна за номер для проживання 3-х осіб)"  # comment to the price

    elif persons == 4:
        rooms_show = rooms.filter(persons__gte=persons)
        for item in rooms_show:
            item.price_comment = "(ціна за номер для проживання 4-х осіб)"  # comment to the price

    elif persons == 10:
        rooms_show = rooms.filter(with_pets=True)  # filtered rooms by "with_pets" value
        for item in rooms_show:
            if item.price_pets:  # if price for living with pets for this room is exist (is filled)
                item.price = item.price_pets  # usual price of the room is replaced
            item.price_comment = "(ціна за номер для проживання з домашніми улюбленцями)"  # price comment
    else:
        rooms_show = rooms

    return rooms_show
######################################################################################################
# # tkinter message window
# window = tkinter.Tk()
#
# # window geometry
# window_height = 250
# window_width = 450
# screen_width = window.winfo_screenwidth()  # gets the value of the width of the user`s screen
# screen_height = window.winfo_screenheight()  # gets the value of the height of the user`s screen
# x_coordinate = int((screen_width / 2) - (window_width / 2))
# y_coordinate = int((screen_height / 2) - (window_height / 2))
# window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
#
# window.resizable(False, False)  # to make the window with a fixed size
# window.attributes('-topmost', 1)  # to put window at the top of the stacking order
#
# def close_win():
#     window.destroy()
#
# window.title("Садиба «Леонтія»")
# label = tkinter.Label(window, text="Вітаємо!\nЗаявку успішно надіслано!\n\n"
#                                    "Невдовзі Вам зателефонує адміністратор", font=("Arial", 14),
#                       fg="#483D8B"
#                       )
# label.pack(padx=20, pady=30)
#
# button = tkinter.Button(window, text="Гаразд", font=("Roboto", 12), foreground="#FFFFFF", command=close_win,
#                         background="#483D8B"
#                         )
# button.pack(pady=20)
#
# window.mainloop()

# messagebox.showinfo("Бронювання", "Заявка надіслана успішно, невдовзі Вам зателефонує адміністратор")
######################################################################################################
