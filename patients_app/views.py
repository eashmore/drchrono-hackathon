from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, QueryDict
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

import requests
import datetime

from models import Doctor, Patient, Problem, Medication, Allergy
from utils import (send_message, send_update_message, send_create_mail,
                   date_to_str, num_to_str)
from api_helper import get_drchrono_user
from forms import PatientForm, ProblemForm, AllergyForm, MedicationForm
from drchrono_patients.settings import CLIENT_DATA


def login_view(request):
    context = {
        'client_id': CLIENT_DATA['client_id'],
        'redirect_url': CLIENT_DATA['redirect_url'],
    }

    return render(request, 'patients_app/sessions/login.html', context)


def oauth_view(request):
    if request.method == 'GET':
        if 'error' in request.GET:
            return redirect('patients_app:login_error')

        user = get_drchrono_user(request.GET)
        auth_user = authenticate(
            username=user.username,
            password=user.doctor.set_random_password()
        )
        login(request, auth_user)
        return redirect('patients_app:home')


def logout_view(request):
    logout(request)
    return redirect('patients_app:login')


def login_error_view(request):
    return render(request, 'patients_app/sessions/login_error.html')


def home_view(request):
    if request.method == 'POST':
        patients = Patient.objects.all()
        patient = find_patient(patients, request.POST)
        if patient is None:
            messages.error(request, 'Patient was not found.')
        else:
            doctor = request.user.doctor
            doctor.current_patient_id = patient.id
            doctor.save()
            return redirect('patients_app:patient_edit')

    doctor = request.user.doctor
    doctor.current_patient_id = None
    doctor.save()
    return render(request, 'patients_app/index.html')


def find_patient(patients, data):
    patient = patients.filter(
        last_name=data['last_name'],
        first_name=data['first_name'],
        social_security_number__endswith=data['ssn']
    )
    if patient.exists():
        return patient.first()

    return None


def patient_view(request):
    patient = Patient.objects.get(pk=request.user.doctor.current_patient_id)
    return render(request, 'patients_app/patient.html', {'patient': patient})


def patient_logout(request):
    doctor = request.user.doctor
    doctor.current_patient_id = None
    doctor.save()
    return redirect('patients_app:home')


def message_view(request):
    patient = Patient.objects.get(pk=request.user.doctor.current_patient_id)
    if (request.method == "POST"):
        doctor_email = request.user.email
        send_message(doctor_email, request.POST['body'], patient)
        messages.success(request, 'Message sent!')
        return redirect('patients_app:message')

    message = 'Hi Dr. {0}, \n\n\n\nBest Regards,\n{1} {2}'.format(
        request.user.last_name, patient.first_name, patient.last_name
    )
    return render(request, 'patients_app/message.html', {'message': message})


def problems_view(request):
    patient = Patient.objects.get(pk=request.user.doctor.current_patient_id)
    problems = patient.problem_set.all()
    return render(request, 'patients_app/problems/problem_index.html', {
        'problems': problems
    })


def problem_edit_view(request, **kwargs):
    problem = get_object_or_404(Problem, pk=kwargs['pk'])
    return render(request, 'patients_app/problems/problem_form.html', {
        'problem': problem,
        'onset_date': date_to_str(problem.date_onset),
        'diagnosis_date': date_to_str(problem.date_diagnosis),
        'method': 'PATCH',
    })


def add_problem_view(request):
    return render(request, 'patients_app/problems/problem_form.html', {
        'onset_date': datetime.date.today().isoformat(),
        'diagnosis_date': datetime.date.today().isoformat(),
        'method': 'POST',
    })


def allergies_view(request):
    patient = Patient.objects.get(pk=request.user.doctor.current_patient_id)
    allergies = patient.allergy_set.all()
    return render(request, 'patients_app/allergies/allergy_index.html', {
        'allergies': allergies
    })


def allergy_edit_view(request, **kwargs):
    allergy = get_object_or_404(Allergy, pk=kwargs['pk'])
    return render(request, 'patients_app/allergies/allergy_form.html', {
        'allergy': allergy,
        'method': 'PATCH',
    })


def add_allergy_view(request):
    return render(request, 'patients_app/allergies/allergy_form.html', {
        'method': 'POST',
    })


def medications_view(request):
    patient = Patient.objects.get(pk=request.user.doctor.current_patient_id)
    medications = patient.medication_set.all()
    return render(request, 'patients_app/medications/med_index.html', {
        'medications': medications
    })


def medication_edit_view(request, **kwargs):
    medication = get_object_or_404(Medication, pk=kwargs['pk'])
    return render(request, 'patients_app/medications/med_form.html', {
        'medication': medication,
        'date_prescribed': date_to_str(medication.date_prescribed),
        'date_started_taking': date_to_str(medication.date_started_taking),
        'date_stopped_taking,': date_to_str(medication.date_stopped_taking),
        'dispense_quantity': num_to_str(medication.dispense_quantity),
        'dosage_quantity': num_to_str(medication.dosage_quantity),
        'number_refills': num_to_str(medication.number_refills),
        'method': 'PATCH',
    })


def add_medication_view(request):
    return render(request, 'patients_app/medications/med_form.html', {
        'date_prescribed': datetime.date.today().isoformat(),
        'date_started_taking': datetime.date.today().isoformat(),
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
                self.post_to_drchrono_api(request, kwargs['pk'])
                messages.success(request, 'Save Successful')
            else:
                messages.success(request, 'Save Failed')

            return redirect('patients_app:patient_edit')

    def post_to_drchrono_api(self, request, patient_id):
        url = 'https://drchrono.com/api/patients/%s' % patient_id
        token = request.user.doctor.token
        header = {'Authorization': 'Bearer %s' % token}
        response = requests.patch(
            url=url, data=request.POST, headers=header
        )
        response.raise_for_status()


class Problem_Index_View(generic.ListView):
    model = Problem
    form_class = ProblemForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.set_additional_attrs(request)
            problem.save()
            send_create_mail(request.user.email, problem)
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
            problem.set_dates(data)
            problem.save()
            send_update_message(
                request.user.email, problem, old_data
            )
            problemJSON = serializers.serialize("json", [problem])
            return HttpResponse(problemJSON, content_type='application/json')

        return HttpResponse(status=500)


class Allergy_Index_View(generic.ListView):
    model = Allergy
    form_class = AllergyForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.set_patient(request.user.doctor.current_patient_id)
            allergy.save()
            send_create_mail(request.user.email, allergy)
            messages.success(request, 'Save Successful')
            return redirect('patients_app:allergy_edit', allergy.id)
        else:
            messages.success(request, 'Save Failed')

        return render(request, 'patients_app/allergies/allergy_form.html', {
            'method': 'POST',
        })


class AllergyView(generic.DetailView):
    model = Allergy
    form_class = AllergyForm

    def get(self, request, **kwargs):
        allegy = get_object_or_404(Allergy, pk=kwargs['pk'])
        allegyJSON = serializers.serialize("json", [allegy])
        return HttpResponse(allegyJSON, content_type='application/json')

    def patch(self, request, **kwargs):
        allegy = get_object_or_404(Allergy, pk=kwargs['pk'])
        old_data = model_to_dict(allegy)
        data = QueryDict(request.body)
        form = self.form_class(data, instance=allegy)
        if form.is_valid():
            allegy = form.save(commit=False)
            allegy.save()
            send_update_message(request.user.email, allegy, old_data)
            allegyJSON = serializers.serialize("json", [allegy])
            return HttpResponse(allegyJSON, content_type='application/json')

        return HttpResponse(status=500)


class Medication_Index_View(generic.ListView):
    model = Medication
    form_class = MedicationForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.set_additional_attrs(request)
            medication.save()
            send_create_mail(request.user.email, medication)
            messages.success(request, 'Save Successful')
            return redirect('patients_app:medication_edit', medication.id)
        else:
            messages.success(request, 'Save Failed')

        return render(request, 'patients_app/medications/med_form.html', {
            'date_prescribed': datetime.date.today().isoformat(),
            'date_started_taking': datetime.date.today().isoformat(),
            'method': 'POST',
        })


class MedicationView(generic.DetailView):
    model = Medication
    form_class = MedicationForm

    def get(self, request, **kwargs):
        medication = get_object_or_404(Medication, pk=kwargs['pk'])
        medicationJSON = serializers.serialize("json", [medication])
        return HttpResponse(medicationJSON, content_type='application/json')

    def patch(self, request, **kwargs):
        medication = get_object_or_404(Medication, pk=kwargs['pk'])
        old_data = model_to_dict(medication)
        data = QueryDict(request.body)
        form = self.form_class(data, instance=medication)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.set_dates(data)
            medication.save()
            send_update_message(request.user.email, medication, old_data)
            medicationJSON = serializers.serialize("json", [medication])
            return HttpResponse(medicationJSON,
                                content_type='application/json')

        return HttpResponse(status=500)


class DoctorView(generic.DetailView):
    model = Doctor

    def get(self, request, **kwargs):
        doctor = get_object_or_404(User, pk=kwargs['pk']).doctor
        doctorJSON = serializers.serialize("json", [doctor])
        return HttpResponse(doctorJSON, content_type='application/json')
