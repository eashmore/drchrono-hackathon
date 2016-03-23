from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.contrib import messages

import string
import random

from models import Patient, Problem, Medication, Allergies
from utils import get_drchrono_user
from forms import PatientForm
from drchrono_patients.settings import CLIENT_DATA


def login_view(request):
    context = {
        'client_id': CLIENT_DATA['client_id'],
        'redirect_url': CLIENT_DATA['redirect_url'],
    }

    return render(request, 'patients_app/login.html', context)


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
        return redirect('patients_app:home')


def logout_view(request):
    logout(request)
    return redirect('patients_app:login')

def home_view(request):
    if request.method == 'POST':
        patients = Patient.objects.all()
        patient = patients.filter(
            last_name=request.POST['last_name'],
            first_name=request.POST['first_name'],
            social_security_number__endswith=request.POST['ssn']
        )
        if patient.exists():
            return redirect('patients_app:patient', patient.first().id)
        else:
            messages.error(request, 'Patient was not found.')

    return render(request, 'patients_app/index.html')


class PatientView(generic.DetailView):
    model = Patient
    template_name = 'patients_app/patient.html'
    form_class = PatientForm

    def get_context_data(self, **kwargs):
        # import pdb; pdb.set_trace()
        context = super(PatientView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=kwargs['object'])
        return context
