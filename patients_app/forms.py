from django import forms

from models import Patient, Problem, Medication, Allergy

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ['doctor', 'social_security_number', 'first_name',
                   'last_name', 'middle_name']

class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ['status', 'notes', 'name', 'description']

class MedicationForm(forms.ModelForm):

    class Meta:
        model = Medication
        exclude = ['patient', 'doctor', 'order_status', 'date_prescribed',
                   'date_started_taking', 'date_stopped_taking']

class AllergyForm(forms.ModelForm):

    class Meta:
        model = Allergy
        exclude = ['patient']
