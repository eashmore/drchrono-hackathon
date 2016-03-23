from django import forms

from models import Patient, Problem, Medication, Allergies

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ['doctor']

class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        exclude = ['patient']

class MedicationForm(forms.ModelForm):

    class Meta:
        model = Medication
        exclude = ['patient']

class AllergiesForm(forms.ModelForm):

    class Meta:
        model = Allergies
        fields = '__all__'
