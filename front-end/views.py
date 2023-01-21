from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
#from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from accounts.models import PhoneNumber, Post
from .forms import  PostForm, UserPhoneNumberForm, UserForm


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
                messages(request, "<p>Vous avez deja un compte avec cet email </p>")
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages(request, "<p> Les deux mots de passe ne sont pas identiques </p>")

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
                username = phone.user.username

        user = authenticate(request, email=username, password=password)
        #test = get_current_site(request)

        if user is not None:
            login(request, user)
            return HttpResponse('successfully logged in !!')

        else:
            return HttpResponse("<p> Vous n'avez pas encore de compte ou"
                                " vos identifiants ne sont pas corrects ")

    return render(request, 'forms/login.html')

@login_required(login_url='/connexion')
def post_form(request):
    User = get_user_model()
    post = PostForm()
    if request.method == 'POST':
        post = PostForm(request.POST, request.FILES)

        if post.is_valid() and User.objects.filter(email=request.user).exists():
            user = User.objects.get(email=request.user)
            post = Post(
                name=post.cleaned_data['name'],
                user_id=user.id,
                price=post.cleaned_data['price'],
                description=post.cleaned_data['description'],
                type_immobilier=post.cleaned_data['type_immobilier'] if post.cleaned_data['type_immobilier'] != '' else None,
                type_automobile=post.cleaned_data['type_automobile'] if post.cleaned_data['type_automobile'] != '' else None,
                category=post.cleaned_data['category'],
                area=post.cleaned_data['area'],
                city=post.cleaned_data['city'],
                image=post.cleaned_data['image']
            )
            post.save()

            return HttpResponse('Vous avez réussi à poster votre poste')

    return render(request, 'forms/post.html', {'post': post})

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
                        send_mail(subject, email, 'schonefeld.dev@gmail.com',
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