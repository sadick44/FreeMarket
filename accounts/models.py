from django.db import models
from django.contrib.auth.models import User


# class Post(models.Model):
#     name = models.CharField(max_length=100)
#     user_post = models.ForeignKey(User, on_delete=models.CASCADE)
#     price = models.FloatField(default=None)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#     description = models.CharField(max_length=100000)
#     phone_number = models.CharField(max_length=10000)
#     image = models.ImageField(upload_to='files')


class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(unique=True)