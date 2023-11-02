from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from GreatKart import settings
from carts.views import cart_id
from carts.models import Cart, CartItem

from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth

import requests


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email, password=password, username=username)
            user.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email_from = settings.EMAIL_HOST_USER
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_mail(mail_subject, message, email_from, [to_email])
            # messages.success(request, 'Thank you for registering. To activate your account verify your email through '
            #                           'email sent to your account')

            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=cart_id(request))
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # getting product variation by car id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
            # cart item from user
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        # this is product variation
                        if pr in ex_var_list:
                            # 'This is from inside existing list'
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            # "Item :- {item}"
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            # 'This is from else block'
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in. ')
            url = request.META.get("HTTP_REFERER")
            print(url)
            try:

                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                # "Params :--->", params
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)


            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out. ')

    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('accounts/reset_password_validate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email_from = settings.EMAIL_HOST_USER
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_mail(mail_subject, message, email_from, [to_email])

            messages.success(request, 'Password reset email has been sent to your account')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid

        messages.success(request, 'Congratulations! your password has been reset.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('forgot_password')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset! please login')

            return redirect('login')
        else:
            messages.error(request, 'password does not match!')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')
