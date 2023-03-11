from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


#slug
urlpatterns = [
    path('', home, name='home'),
    path('compte', user_register, name="signup"),
    path('connexion', user_login, name='login'),
    path('create-post', post_form, name='post'),
    path('password_reset', password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),      
    path('posts', post_display, name='all_posts'),
    path('post/<int:pk>', single_post, name='single_post'),
    path('deconnexion', user_logout, name='logout'),
    path('results', user_search, name="user_search")
 #   path('favorites_posts/<int:pk>', add_to_favorite, name='favorite_posts'),
]