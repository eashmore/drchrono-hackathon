from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, QueryDict
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

import string
import random
import requests
import datetime

from models import Doctor, Patient, Problem, Medication, Allergies
from utils import get_drchrono_user, send_message, send_update_message
from forms import PatientForm, ProblemForm
from drchrono_patients.settings import CLIENT_DATA


def login_view(request):
    context = {
        'client_id': CLIENT_DATA['client_id'],
        'redirect_url': CLIENT_DATA['redirect_url'],
    }

    return render(request, 'patients_app/login.html', context)


def oauth_view(request):
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


def set_random_password(user):
    all_chars = string.letters + string.digits + string.punctuation
    password = ''.join((random.choice(all_chars)) for x in range(20))
    user.set_password(password)
    user.save()
    return password


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
            doctor = request.user.doctor
            doctor.current_patient_id = patient.first().id
            doctor.save()
            return redirect('patients_app:patient_edit')
        else:
            messages.error(request, 'Patient was not found.')

    return render(request, 'patients_app/index.html')


def patient_view(request):
    patient = get_object_or_404(
        Patient, pk=request.user.doctor.current_patient_id
    )

    return render(request, 'patients_app/patient.html', {'patient': patient})


def patient_logout(request):
    doctor = request.user.doctor
    doctor.current_patient_id = None
    doctor.save()
    return redirect('patients_app:home')


def message_view(request):
    if (request.method == "POST"):
        doctor_email = request.user.email
        patient = get_object_or_404(
            Patient, pk=request.user.doctor.current_patient_id
        )
        send_message(doctor_email, request.POST['body'], patient)
        messages.success(request, 'Message sent!')
        return redirect('patients_app:message')

    return render(request, 'patients_app/message.html')


def problems_view(request):
    patient = get_object_or_404(
        Patient, pk=request.user.doctor.current_patient_id
    )
    problems = patient.problem_set.all()
    return render(request, 'patients_app/problems/problem_index.html', {
        'problems': problems
    })


def problem_edit_view(request, **kwargs):
    problem = get_object_or_404(Problem, pk=kwargs['pk'])
    onset_date = get_date_str(problem.date_onset)
    diagnosis_date = get_date_str(problem.date_diagnosis)
    return render(request, 'patients_app/problems/problem_form.html', {
        'problem': problem,
        'onset_date': onset_date,
        'diagnosis_date': diagnosis_date,
        'method': 'PATCH',
    })


def get_date_str(date):
    if date:
        return date.isoformat()
    else:
        return datetime.date.today().isoformat()


def add_problem_view(request):
    return render(request, 'patients_app/problems/problem_form.html', {
        'onset_date': datetime.date.today().isoformat(),
        'diagnosis_date': datetime.date.today().isoformat(),
        'method': 'POST',
    })


class PatientView(generic.DetailView):
    model = Patient
    form_class = PatientForm

    def post(self, request, **kwargs):
        if request.POST['_method'] == 'PATCH':
            patient = get_object_or_404(Patient, pk=kwargs['pk'])
            form = self.form_class(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                url = 'https://drchrono.com/api/patients/%s' % kwargs['pk']
                token = request.user.doctor.token
                header = {'Authorization': 'Bearer %s' % token}
                response = requests.patch(url=url, data=request.POST, headers=header)
                response.raise_for_status()
                messages.success(request, 'Save Successful')
            else:
                messages.success(request, 'Save Failed')

            return redirect('patients_app:patient_edit')


class Problem_Index_View(generic.DetailView):
    model = Problem
    form_class = ProblemForm

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.date_onset = datetime.datetime.strptime(
                request.POST['date_onset'], '%Y-%m-%d')
            problem.date_diagnosis = datetime.datetime.strptime(
                request.POST['date_diagnosis'], '%Y-%m-%d')
            patient = get_object_or_404(
                Patient, pk=request.user.doctor.current_patient_id
            )
            problem.patient = patient
            problem.save()
            doctor_email = request.user.email
            send_update_message(doctor_email, patient, problem)
            messages.success(request, 'Save Successful')
            return redirect('patients_app:problem_edit', problem.id)
        else:
            messages.success(request, 'Save Failed')

        return render(request, 'patients_app/problems/problem_form.html', {
            'onset_date': datetime.date.today().isoformat(),
            'diagnosis_date': datetime.date.today().isoformat(),
            'method': 'POST',
        })


class ProblemView(generic.DetailView):
    model = Problem
    form_class = ProblemForm

    def get(self, request, **kwargs):
        problem = get_object_or_404(Problem, pk=kwargs['pk'])
        problemJSON = serializers.serialize("json", [problem])
        return HttpResponse(problemJSON, content_type='application/json')

    def patch(self, request, **kwargs):
        problem = get_object_or_404(Problem, pk=kwargs['pk'])
        old_data = model_to_dict(problem)
        data = QueryDict(request.body)
        form = self.form_class(data, instance=problem)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.date_onset = datetime.datetime.strptime(
                data['date_onset'], '%Y-%m-%d')
            problem.date_diagnosis = datetime.datetime.strptime(
                data['date_diagnosis'], '%Y-%m-%d')
            problem.save()
            doctor_email = request.user.email
            patient = get_object_or_404(
                Patient, pk=request.user.doctor.current_patient_id
            )
            send_update_message(doctor_email, patient, problem, old_data)
            problemJSON = serializers.serialize("json", [problem])
            return HttpResponse(problemJSON, content_type='application/json')

        return HttpResponse(status=500)

# class DoctorView(generic.DetailView):
#     model = Doctor
#
#     def get(self, request, **kwargs):
#         doctor = get_object_or_404(User, pk=kwargs['pk']).doctor
#         doctorJSON = serializers.serialize("json", [doctor])
#         doctorJSON = doctorJSON[1:len(doctorJSON) - 1]
#         return HttpResponse(doctorJSON, content_type='application/json')
