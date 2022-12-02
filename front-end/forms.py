from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from accounts.models import PhoneNumber, Post
from accounts.constants.constants import *


class UserModelForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"name": "password1", 'placeholder': 'Mot de passe', 'class': 'form-control'}), label='Mot de passe')

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"name": "password2", 'placeholder': 'Confirmer mot de passe', 'class': 'form-control'}),
        label='Confirmer mot de passe')

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
        attrs={"class": "form-control", "name": "phone_number", "placeholder": "Numero de téléphone"}), label='Numéro de téléphone')

    class Meta:
        model = PhoneNumber
        fields = ['phone_number']


class PostForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={"name": "post",
    "placeholder": 'Nom de votre article', 'required': True,
                                      "class": "form-control-sm pr-4", 'style': 'width:100%'}), label='Nom')

    price = forms.CharField(widget=forms.NumberInput(attrs={
        "name": "price", "help": "prix",
        "class": "form-control-sm", "style": "width:100%"}), label='Prix')

    description = forms.CharField(widget=forms.Textarea(
        attrs={'name': 'description', 'placeholder': 'description',
               "class": "form-control-sm", 'style': 'width:100%'}), label='Description')

    type_immobilier = forms.ChoiceField(choices=TYPES_IMMOBILIER)
    type_automobile = forms.ChoiceField(choices=TYPES_AUTOMOBILE)
    category = forms.ChoiceField(choices=CATEGORIES)
    area = forms.CharField(widget=forms.TextInput(
        attrs={'name': 'area', "class": "form-control-sm", 'style': 'width:100%'}), label='Quartier')

    city = forms.CharField(widget=forms.TextInput(
        attrs={'name': 'city', "class": "form-control-sm", 'style': 'width:100%'}), label='Ville')

    class Meta:
        model = Post
        fields = ['name', 'price', 'area', 'category', 'city', 'type_automobile','type_immobilier', 'description']