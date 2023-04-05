import telebot


# the logic of the room price policy and the function of informing the staff are written here

def message_telegram(reservation):
    # informing the staff about the new reservation request via telegram
    TOKEN = '5683712081:AAHOCCORZKYWHcnZ72U2nhnjK0h42HToBYY'
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(
        "703984335",
        f'{reservation.phone} | Бронювання: {reservation.name}; {reservation.room.inn_number} '
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
    :return: filtered rooms objects (with actual prices).
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
