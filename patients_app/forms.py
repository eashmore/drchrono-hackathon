from django import forms

from models import Patient, Problem, Medication, Allergies

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
        exclude = ['patient']

class AllergiesForm(forms.ModelForm):

    class Meta:
        model = Allergies
        fields = '__all__'
