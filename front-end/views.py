from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserPhoneNumberForm
from accounts.models import PhoneNumber
from .forms import UserModelForm
from accounts.models import MultipleImage


def home(request):
    return render(request, 'home.html')


def user_register(request):
    form = UserModelForm()
    userform = UserPhoneNumberForm()

    if request.method == 'POST':
        form = UserModelForm(request.POST)
        userform = UserPhoneNumberForm(request.POST)

        if form.is_valid() and userform.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages(request, "<p>Vous avez deja un compte avec cet email </p>")

            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages(request, "<p> Les deux mots de passe ne sont pas identiques </p>")

            else:
                user = User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password1'])
                user.save()
                current_user_id = User.objects.get(username=form.cleaned_data['username']).id
                phone_number_user = PhoneNumber.objects.create(user_id=current_user_id,
                                                               phone_number=userform.cleaned_data['phone_number'])
                phone_number_user.save()

                return redirect('/')

    return render(request, 'forms/signup.html', {'form': form, 'userform': userform})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        #test = get_current_site(request)

        if user is not None:
            login(request, user)
            return HttpResponse('successfully logged in !!')

    return render(request, 'forms/login.html')


def upload(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            MultipleImage.objects.create(images=image)
    images = MultipleImage.objects.all()
    return render(request, 'forms/multi-images.html', {'images': images})