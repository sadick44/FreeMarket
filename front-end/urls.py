from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', home, name='home'),
    path('compte', user_register, name="signup"),
    path('connexion', user_login, name='login'),
    path('checkimage', upload, name='multi-images' ),

    path("password_reset/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("password_reset/done", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]