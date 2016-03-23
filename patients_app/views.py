from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

import string
import random

from drchrono_patients.settings import CLIENT_DATA
from utils import get_drchrono_user


def login_view(request):
    context = {
        'client_id': CLIENT_DATA['client_id'],
        'redirect_url': CLIENT_DATA['redirect_url'],
    }

    return render(request, 'accounts_app/login.html', context)


def oauth_view(request):
    def set_random_password(user):
        all_chars = string.letters + string.digits + string.punctuation
        password = ''.join((random.choice(all_chars)) for x in range(20))
        user.set_password(password)
        user.save()
        return password

    if request.method == 'GET':
            # if 'error' in request.GET:
                # return redirect('patients_app:login_error')

        user = get_drchrono_user(request.GET)
        auth_user = authenticate(
            username=user.username,
            password=set_random_password(user)
        )
        login(request, auth_user)
        return redirect('patients_app:home_view')


def logout_view(request):
    logout(request)
    return redirect('account_app:login')
