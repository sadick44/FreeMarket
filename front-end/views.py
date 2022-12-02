from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import PhoneNumber, MultipleImage, Post
from .forms import UserModelForm, PostForm, UserPhoneNumberForm


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


def post_form(request):
    post = PostForm()
    if request.method == 'POST':
        post = PostForm(request.POST)
        if post.is_valid():
            post = Post.objects.create(
                name=post.cleaned_data['name'],
                user_post=request.user,
                price=post.cleaned_data['price'],
                description=post.cleaned_data['description'],
                type=post.cleaned_data['type'] if post.cleaned_data['type'] != '' else None,
                category=post.cleaned_data['category'] if post.cleaned_data['category'] != '' else None,
                area=post.cleaned_data['area'],
                city=post.cleaned_data['city']

            )
            post.save()

            return HttpResponse('Vous réussi à poster votre poste')

    return render(request, 'forms/post.html', {'post': post})