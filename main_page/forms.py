from django import forms
from main_page.models import Reservation


class RoomReservationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Прізвище"}), required=False)
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
    room_id = forms.IntegerField(widget=forms.IntegerField, disabled=True)
    room_price = forms.DecimalField(max_digits=6, decimal_places=2, disabled=True)
    user_id = forms.IntegerField(required=False, disabled=True)
    # user_email = forms.CharField(widget=forms.CharField)

    class Meta:
        model = Reservation
        fields = ["name", "last_name", "phone", "message", "persons", "room_id", "room_price", "user_id"]


