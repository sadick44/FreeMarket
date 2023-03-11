from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
#from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from accounts.models import PhoneNumber, Post
from .forms import  PostForm, UserPhoneNumberForm, UserForm
from django.contrib.auth import get_user_model

from accounts.models import PhoneNumber, Post, Image, UserSearch
from .forms import  PostForm, UserPhoneNumberForm, UserForm, ImageForm

User = get_user_model()

def home(request):
    if request.method == 'POST':
        word_searched = request.POST["word"]
        user = request.user if request.user is authenticate else None
        user_input = UserSearch.objects.create(word_entered=word_searched, user=user)
        user_input.save()

        results = Image.objects.filter(post__name__icontains=word_searched)\
            .filter(post__description__icontains=word_searched).distinct('id')[::2]

        # results = Post.objects.filter(name__icontains=word_searched).order_by('-created_date')\
        #                     .values('image__images', 'name', 'price')[::2]

        return render(request, 'internal/search.html', {'results': results,
                                                        'data_length': len(results), 'word_searched': word_searched})
    return render(request, 'home.html')


def getPostById(id):
    return Post.objects.get(id=id)

def getUserByEmail(email):
    return User.objects.get(email=email)

def user_register(request):
    form = UserForm()
    userform = UserPhoneNumberForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        userform = UserPhoneNumberForm(request.POST)

        if form.is_valid() and userform.is_valid():

            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.warning(request, "Vous avez deja un compte avec cet email")

            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.warning(request, "Les deux mots de passe ne sont pas identiques")

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

                return redirect(request.GET.get('next', '/'))

    return render(request, 'forms/signup.html', {'form': form, 'userform': userform})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if '@' not in username and not  username.isnumeric():
            messages.warning(request, "Entrez votre mail ou numero de téléphone")
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


@login_required(login_url='/connexion')
def post_form(request):
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

def password_reset_request(request):
    User = get_user_model()
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"  # noqa
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Emarket',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'carrefourhanana.dev@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset/done")
    password_reset_form = PasswordResetForm()
    context = {
        'password_reset_form': password_reset_form
    }
    return render(request=request, context=context,
                  template_name="registration/password_reset_form.html")


login_required(login_url="/connexion")
def user_profile(request):
    pass

def post_display(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})

def single_post(request, pk):

    post = getPostById(id=pk)
    images = Image.objects.filter(post=post)
    user = post.user
    user = getUserByEmail(user)
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

# @login_required(login_url='/connexion')
# def add_to_favorite(request, pk):
#     post = getPostById(id=pk)
#     user = getUserByEmail(email=request.user)
#
#     if not FavoritePost.objects.filter(post=post).exists():
#         add_favorite = FavoritePost.objects.create(post=post, user=user)
#         add_favorite.save()
#
#     myFavoritesPosts = FavoritePost.objects.filter(user=user)
#       hunter.io
        # phonebook.cz
        # recrutement@acxa-juridica.com
#     return render(request, 'internal/favorites.html',
#                   {
#                       'post': post, 'myFavoritesPosts': myFavoritesPosts
#                   })

def user_search(request):

    return render(request, 'home.html')
