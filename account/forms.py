from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    """Form for login to personal user`s account."""
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
    """Form for registration personal user`s account."""
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я"}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть прізвище"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я для входу"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Адреса електронної скриньки"}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Придумайте та введіть пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть пароль ще раз"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    """Form for show and update personal user`s account information."""
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', "readonly": True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone")
