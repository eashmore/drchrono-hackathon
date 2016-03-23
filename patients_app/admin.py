from django.contrib import admin

from models import Patient, Problem, Medication, Allergy

admin.site.register(Patient)
admin.site.register(Problem)
admin.site.register(Medication)
admin.site.register(Allergy)
