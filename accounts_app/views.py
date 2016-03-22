from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from drchrono_patients.settings import CLIENT_DATA
from utils import get_drchrono_user

def login_view(request):
    if request.method == 'GET':
            # if 'error' in request.GET:
                # return redirect('patients_app:login_error')

        user = get_drchrono_user(request.GET)
        auth_user = authenticate(
            username=user.username,
            password=user.doctor.set_random_password()
        )
        login(request, auth_user)
        return redirect('drchrono_birthdays:index_view')

    context = {
        'client_id': CLIENT_DATA['client_id'],
        'redirect_url': CLIENT_DATA['redirect_url'],
    }

    return render(request, 'accounts_app/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('account_app:login')
