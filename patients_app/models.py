from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import string
import random

from utils import str_to_date


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    token = models.CharField(max_length=200)
    current_patient_id = models.IntegerField(null=True, blank=True)

    def set_random_password(self):
        user = self.user
        all_chars = string.letters + string.digits + string.punctuation
        password = ''.join((random.choice(all_chars)) for x in range(20))
        user.set_password(password)
        user.save()
        return password


class Patient(models.Model):
    doctor = models.ForeignKey(User)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    home_phone = models.CharField(max_length=14, blank=True)
    cell_phone = models.CharField(max_length=14, blank=True)
    city = models.CharField(max_length=200, blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=200, blank=True)
    emergency_contact_relation = models.CharField(max_length=200, blank=True)
    employer = models.CharField(max_length=200, blank=True)
    employer_city = models.CharField(max_length=200, blank=True)
    employer_address = models.CharField(max_length=200, blank=True)
    employer_state = models.CharField(max_length=200, blank=True)
    employer_zip_code = models.CharField(blank=True, max_length=200)
    primary_care_physician = models.CharField(
        max_length=200, blank=True, null=True
    )
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    social_security_number = models.CharField(max_length=20, blank=True)
    responsible_party_name = models.CharField(max_length=200, blank=True)
    responsible_party_phone = models.CharField(max_length=14, blank=True)
    responsible_party_relation = models.CharField(max_length=200, blank=True)
    responsible_party_email = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

    @classmethod
    def column_list(cls):
        cols = ['doctor', 'first_name', 'middle_name', 'last_name', 'address',
                'email', 'home_phone', 'cell_phone', 'city', 'zip_code',
                'emergency_contact_name', 'emergency_contact_phone', 'state',
                'emergency_contact_relation', 'employer', 'employer_city',
                'employer_state', 'employer_address', 'primary_care_physician',
                'social_security_number', 'responsible_party_name',
                'responsible_party_phone', 'responsible_party_relation',
                'responsible_party_email']
        return cols


class Problem(models.Model):
    patient = models.ForeignKey(Patient)
    date_changed = models.DateField(null=True, blank=True)
    date_diagnosis = models.DateField(null=True, blank=True)
    date_onset = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    def set_additional_attrs(self, request):
        self.set_patient(request.user.doctor.current_patient_id)
        self.set_dates(request.POST)

    def set_patient(self, patient_id):
        patient = Patient.objects.get(pk=patient_id)
        self.patient = patient

    def set_dates(self, data):
        self.date_onset = str_to_date(data['date_onset'])
        self.date_diagnosis = str_to_date(data['date_diagnosis'])


class Medication(models.Model):
    doctor = models.ForeignKey(User)
    patient = models.ForeignKey(Patient)
    daw = models.BooleanField()
    name = models.CharField(max_length=200)
    prn = models.BooleanField()
    date_prescribed = models.DateField(null=True, blank=True)
    date_started_taking = models.DateField(null=True, blank=True)
    date_stopped_taking = models.DateField(null=True, blank=True)
    dispense_quantity = models.FloatField(null=True, blank=True)
    dosage_quantity = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    frequency = models.CharField(max_length=200, blank=True)
    number_refills = models.IntegerField(blank=True, null=True)
    order_status = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    def set_additional_attrs(self, request):
        self.doctor = request.user
        self.set_patient(request.user.doctor.current_patient_id)
        self.set_dates(request.POST)

    def set_patient(self, patient_id):
        patient = Patient.objects.get(pk=patient_id)
        self.patient = patient

    def set_dates(self, data):
        self.date_prescribed = str_to_date(data['date_prescribed'])
        self.date_started_taking = str_to_date(data['date_started_taking'])
        self.date_stopped_taking = str_to_date(data['date_stopped_taking'])


class Allergy(models.Model):
    patient = models.ForeignKey(Patient)
    notes = models.TextField(blank=True)
    reaction = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.reaction

    def set_patient(self, patient_id):
        patient = Patient.objects.get(pk=patient_id)
        self.patient = patient


class Insurance(models.Model):
    rank = models.IntegerField()
    payer_name = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    patient = models.ForeignKey(Patient)

    def __str__(self):
        return self.payer_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient)
    scheduled_time = models.CharField(max_length=200)
    status = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.scheduled_time

    class Meta:
        ordering = ['scheduled_time']
