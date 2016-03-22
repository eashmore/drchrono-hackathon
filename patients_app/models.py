from __future__ import unicode_literals

from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
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
    employer_address = models.CharField(max_length=200, blank=True)
    employer_city = models.CharField(max_length=200, blank=True)
    employer_state = models.CharField(max_length=200, blank=True)
    employer_zip_code = models.CharField(max_length=200, blank=True)
    primary_care_physician = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    state = models.CharField(max_length=2, blank=True)
    social_security_number = models.CharField(max_length=20, blank=True)
    responsible_party_name = models.CharField(max_length=200, blank=True)
    responsible_party_phone = models.CharField(max_length=14, blank=True)
    responsible_party_relation = models.CharField(max_length=200, blank=True)
    responsible_party_email = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)


class Problem(models.Model):
    patient = models.ForeignKey('Patient')
    date_changed = models.DateField(blank=True)
    date_diagnosis = models.DateField(blank=True)
    date_onset = models.DateField(blank=True)
    description = models.TextField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=200, blank=True)

class Medication(models.Model):
    doctor_id = models.IntegerField()
    daw = models.BooleanField()
    name = models.CharField(max_length=200)
    prn = models.BooleanField()
    date_prescribed = models.DateField(blank=True)
    date_started_taking = models.DateField(blank=True)
    date_stopped_taking = models.DateField(blank=True)
    dispense_quantity = models.FloatField(blank=True)
    dosage_quantity = models.FloatField(blank=True)
    notes = models.TextField(blank=True)
    frequency = models.CharField(max_length=200)
    number_refills = models.IntegerField()
    order_status = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

class Insurance(models.Model):
    rank = models.IntegerField()
    payer_name = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    patient = models.ForeignKey('Patient')

class Allergies(models.Model):
    description = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    reaction = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, blank=True)
