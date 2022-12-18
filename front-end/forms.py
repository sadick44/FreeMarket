from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import PhoneNumber, Post
from accounts.constants.constants import *

from accounts.models import User


class UserForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"class":"form-control", "name":"first_name"}
    ), label="Votre Prenom")

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"class":"form-control", "name": "last_name"}
    ), label="Votre Nom")

    email=forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control", "name": "email", "style": "width:100%"
    }), label="Votre  email")

    password1 =forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", "name": "password1"
    }), label="Votre mot de passe")

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", "name": "confirm_password"
    }), label="Confirmer votre mot de passe")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

class UserPhoneNumberForm(forms.ModelForm):
    phone_number = forms.IntegerField(widget=forms.NumberInput(
        attrs={"class": "form-control", "name": "phone_number", "placeholder": "Numero de téléphone"}), label='Numéro de téléphone')

    class Meta:
        model = PhoneNumber
        fields = ['phone_number']


class PostForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={"name": "post",
    "placeholder": 'Titre de votre article', 'required': True,
                                      "class": "form-control pr-4", 'style': 'width:100%'}), label='Titre de votre annonce')

    price = forms.CharField(widget=forms.NumberInput(attrs={
        "name": "price", "help": "prix",
        "class": "form-control", "style": "width:100%"}), label='Prix')

    description = forms.CharField(widget=forms.Textarea(
        attrs={'name': 'description', 'placeholder': 'description',
               "class": "form-control", 'style': 'width:100%'}), label='Description')

    type_immobilier = forms.ChoiceField(choices=TYPES_IMMOBILIER, widget=forms.Select(
        attrs={"class": "form-control", "name": "type_immobilier", "style": "width:100%", "required": False}
    ))
    type_automobile = forms.ChoiceField(widget=forms.Select(
        attrs={'name': 'type_automobile', 'class': 'form-control', "required": False}
    ), label='type automobile', choices=TYPES_AUTOMOBILE)
    category = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select(
        attrs={"class": "form-control", "name": "category"}
    ))
    area = forms.CharField(widget=forms.TextInput(
        attrs={'name': 'area', "class": "form-control", 'style': 'width:100%'}), label='Quartier')

    city = forms.CharField(widget=forms.TextInput(
        attrs={'name': 'city', "class": "form-control", 'style': 'width:100%','required': True}), label='Ville')

    image = forms.ImageField(widget=forms.FileInput(
        attrs={"class": "form-control ", "name": "images"}
    ), label="Choisir image(s)")
    class Meta:
        model = Post
        fields = ['name', 'price', 'area', 'category', 'city',
                  'type_automobile','type_immobilier', 'description', 'image']