from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('compte', user_register, name="signup"),
    path('connexion', user_login, name='login'),
    path('create-post', post_form, name='post'),
]