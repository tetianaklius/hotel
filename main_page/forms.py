from django import forms
from main_page.models import Reservation


class RoomReservationForm(forms.ModelForm):
    """
    This form is filled by the user and transmits this input information (name, last name, phone, email, message,
    quantity of persons is needed) and some internal information (room id, room price, user id)
    to the model Reservation. This information needed to send a room reservation request
    to the hotel. The request will be manually processed by the manager.
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Прізвище"}),
                                required=False)
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "type": "text",
        "class": "form-control",
        "name": "phone",
        "id": "phone",
        "placeholder": "Номер телефону",
        "data-rule": "minlen:4",
        "data-msg": "Please enter at least 4 chars"}))

    persons = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': ""
    }))

    message = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "name": "message",
        "rows": "5",
        "placeholder": "Наприклад, коли Вам зручніше, щоб ми зателефонували тощо",
    }))

    room_id = forms.IntegerField(widget=forms.TextInput(attrs={
        'type': "hidden", "class": "form-control", "name": "room_id"}),
        required=False)

    room_price = forms.DecimalField(widget=forms.TextInput(attrs={
        'type': "hidden", "class": "form-control", "name": "room_price"}))

    user_id = forms.IntegerField(widget=forms.TextInput(attrs={
        'type': "hidden", "class": "form-control", "name": "user_id"}),
        required=False)

    user_email = forms.CharField(widget=forms.TextInput(attrs={
        'type': "hidden", "class": "form-control", "name": "user_email"}),
        required=False)

    class Meta:
        model = Reservation
        fields = ["name", "last_name", "phone", "message", "persons", "room_id", "room_price", "user_id"]
