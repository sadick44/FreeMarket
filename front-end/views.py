from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from accounts.models import PhoneNumber, Post, Image
from .forms import  PostForm, UserPhoneNumberForm, UserForm, ImageForm


def home(request):
    return render(request, 'home.html')


def user_register(request):
    form = UserForm()
    userform = UserPhoneNumberForm()
    User = get_user_model()

    if request.method == 'POST':
        form = UserForm(request.POST)
        userform = UserPhoneNumberForm(request.POST)

        if form.is_valid() and userform.is_valid():

            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.add_message(request, messages.warning,
                                     "<p>Vous avez deja un compte avec cet email </p>")

            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.add_message(request,messages.warning,
                                     "<p> Les deux mots de passe ne sont pas identiques </p>")

            else:
                user = User.objects.create_user(email=form.cleaned_data['email'],
                                                        first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],
                                                        password=form.cleaned_data['password1'])
                user.save()
                current_user_id = User.objects.get(email=form.cleaned_data['email']).id
                phone_number_user = PhoneNumber.objects.create(user_id=current_user_id,
                                                               phone_number=userform.cleaned_data['phone_number'])
                phone_number_user.save()

                return redirect('/')

    return render(request, 'forms/signup.html', {'form': form, 'userform': userform})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if '@' not in username:
            phone = PhoneNumber.objects.filter(phone_number=username)
            if phone:
                user = PhoneNumber.objects.get(phone_number=username).user
                username = user.email
        user = authenticate(request, email=username, password=password)
        #test = get_current_site(request)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/')) # redirect the user to home after login or the
                                                          # to previous page where login is required

        else:
            messages.warning(request, "Votre identifiant ou mot de passe n'est pas correct.")
            return render(request, 'forms/login.html')

    return render(request, 'forms/login.html')

@login_required(login_url='/connexion')
def post_form(request):
    User = get_user_model()
    post = PostForm()
    imageform = ImageForm()

    if request.method == 'POST':
        post = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if post.is_valid() and User.objects.filter(email=request.user).exists():
            user = User.objects.get(email=request.user)

            post = post.save(commit=False)
            post.user = user
            post.save()

            for file in files:
                Image.objects.create(post=post, images=file)

            return HttpResponse('Vous avez réussi à poster votre poste')

    return render(request, 'forms/post.html', {'post': post, 'imageform': imageform})


login_required(login_url="/connexion")
def user_profile(request):
    pass

def post_display(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})

def single_post(request, pk):
    User = get_user_model()
    post = Post.objects.get(id=pk)
    images = Image.objects.filter(post=post)
    user = post.user
    user = User.objects.get(email=user)
    first_name = user.first_name
    last_name = user.last_name
    phone_number = PhoneNumber.objects.get(user=user)
    phone_number = phone_number.phone_number

    return render(request, 'internal/productView.html', {'post': post, 'first_name': first_name,
                                                         'last_name': last_name, 'images': images,
                                                         'phone_number': phone_number})

@login_required(login_url='/connexion')
def user_logout(request):
    logout(request)
    return redirect('/')