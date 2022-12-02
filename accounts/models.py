from django.db import models
from django.contrib.auth.models import User
from accounts.constants.constants import *


class Post(models.Model):

    name = models.CharField(max_length=100) #titre du produit
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=10000)
    category = models.CharField(choices=CATEGORIES, max_length=80, blank=True, null=True)
   # image = models.ImageField(upload_to='files')
    type_immobilier = models.CharField(choices=TYPES_IMMOBILIER, max_length=50, blank=True, null=True)
    type_automobile = models.CharField(choices=TYPES_AUTOMOBILE, max_length=50, blank=True, null=True)
    area = models.CharField(max_length=60)
    city = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.phone_number


class MultipleImage(models.Model):
    images = models.FileField()