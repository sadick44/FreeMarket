from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from accounts.models import PhoneNumber


class UserModelForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"name": "password1", 'placeholder': 'Mot de passe', 'class': 'form-control'}), label='')

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"name": "password2", 'placeholder': 'Confirmer mot de passe', 'class': 'form-control'}), label='')

    username = forms.CharField(widget=forms.EmailInput(
        attrs={"name": "username", 'placeholder': 'Email', 'class': 'form-control'}), label='')

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"name": "first_name", 'placeholder': 'Prenom', 'class': 'form-control'}), label='')

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"name": "last_name", 'placeholder': 'Nom', 'class': 'form-control'}), label='')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserPhoneNumberForm(forms.ModelForm):
    phone_number = forms.IntegerField(widget=forms.NumberInput(
        attrs={"class": "form-control", "name": "phone_number", "placeholder": "Numero de téléphone"}), label='')

    class Meta:
        model = PhoneNumber
        fields = ['phone_number']