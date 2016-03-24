from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'patients_app'

urlpatterns = [
    # session
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/oauth/$', views.oauth_view, name='oauth'),
    url(r'^accounts/logout/$', login_required(views.logout_view),
        name='logout'),
    url(r'^accounts/error/$', views.login_error_view,
        name='login_error'),
    url(r'^$', login_required(views.home_view), name='home'),

    # patient
    url(r'^patient/$', login_required(views.patient_view),
        name='patient_edit'),
    url(r'^patient/(?P<pk>[0-9]+)/$',
        login_required(views.PatientView.as_view()), name='patient'),
    url(r'^patient/logout/$', login_required(views.patient_logout),
        name='patient_logout'),
    url(r'^patient/message/$', login_required(views.message_view),
        name='message'),

    # problems
    url(r'^patient/problems/$', login_required(views.problems_view),
        name='problem_list'),
    url(r'^patient/problem/(?P<pk>[0-9]+)/$',
        login_required(views.problem_edit_view), name='problem_edit'),
    url(r'^patient/problems/new$', login_required(views.add_problem_view),
        name='problem_new'),

    # allergies
    url(r'^patient/allergies/$', login_required(views.allergies_view),
        name='allergy_list'),
    url(r'^patient/allergy/(?P<pk>[0-9]+)/$',
        login_required(views.allergy_edit_view), name='allergy_edit'),
    url(r'^patient/allergies/new$', login_required(views.add_allergy_view),
        name='allergy_new'),

    # medications
    url(r'^patient/medications/$', login_required(views.medications_view),
        name='medication_list'),
    url(r'^patient/medication/(?P<pk>[0-9]+)/$',
        login_required(views.medication_edit_view), name='medication_edit'),
    url(r'^patient/medications/new$', login_required(views.add_medication_view),
        name='medication_new'),

    # API
    url(r'^api/problems/$', login_required(views.Problem_Index_View.as_view()),
        name='problem_index'),
    url(r'^api/problem/(?P<pk>[0-9]+)/$',
        login_required(views.ProblemView.as_view()), name='problem'),
    url(r'^api/allergies/$', login_required(views.Allergy_Index_View.as_view()),
        name='allergy_index'),
    url(r'^api/allergy/(?P<pk>[0-9]+)/$',
        login_required(views.AllergyView.as_view()), name='allergy'),
    url(
        r'^api/medications/$',
        login_required(views.Medication_Index_View.as_view()),
        name='medication_index'
    ),
    url(r'^api/medication/(?P<pk>[0-9]+)/$',
        login_required(views.MedicationView.as_view()), name='medication'),
    url(r'^api/doctor/(?P<pk>[0-9]+)/$',
        login_required(views.DoctorView.as_view()), name='doctor'),
]
