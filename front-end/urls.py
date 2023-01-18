from django.urls import path
from .views import *

#slug
urlpatterns = [
    path('', home, name='home'),
    path('compte', user_register, name="signup"),
    path('connexion', user_login, name='login'),
    path('create-post', post_form, name='post'),
    path('posts', post_display, name='all_posts'),
    path('post/<int:pk>', single_post, name='single_post'),
    path('deconnexion', user_logout, name='logout')
]