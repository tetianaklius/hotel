from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control py-4",
        "placeholder": "Введіть ім'я"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control py-4",
        "placeholder": "Введіть пароль"
    }))

    class Meta:
        model = User
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я"}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть прізвище"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я для входу"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Адреса електронної скриньки"}), required=False)
    # phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
    #     "type": "text",
    #     "class": "form-control",
    #     "name": "phone",
    #     "id": "phone",
    #     "placeholder": "Your Phone",
    #     "data-rule": "minlen:4",
    #     "data-msg": "Please enter at least 4 chars"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Придумайте та введіть пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть пароль ще раз"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', "readonly": True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone")
