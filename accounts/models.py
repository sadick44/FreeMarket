from django.db import models
from accounts.constants.constants import *
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    user_type = (
        ('customer', 'customer'),
        ('professionnal', 'professionnal'),
    )

    username = None
    email = models.EmailField(max_length=30, unique=True)
    role = models.CharField(choices=user_type, max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [] # needed later when wanna monetize it

    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    pass


class Post(models.Model):

    name = models.CharField(max_length=100) #titre du produit
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.FloatField(default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=10000)
    category = models.CharField(choices=CATEGORIES, max_length=80, blank=True, null=True)
    type_immobilier = models.CharField(choices=TYPES_IMMOBILIER, max_length=50, blank=True, null=True)
    type_automobile = models.CharField(choices=TYPES_AUTOMOBILE, max_length=50, blank=True, null=True)
    area = models.CharField(max_length=60)
    city = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="images/")


class PhoneNumber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.IntegerField(unique=True)