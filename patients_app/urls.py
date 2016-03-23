from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'patients_app'

urlpatterns = [
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/oauth/$', views.oauth_view, name='oauth'),
    url(r'^accounts/logout/$', login_required(views.logout_view),
        name='logout'),
    url(r'^$', login_required(views.home_view), name='home'),

    url(r'^patient/$', login_required(views.patient_view),
        name='patient_edit'),
    url(r'^patient/(?P<pk>[0-9]+)/$',
        login_required(views.PatientView.as_view()), name='patient'),
    url(r'^patient/logout/$', login_required(views.patient_logout),
        name='patient_logout'),
    url(r'^patient/message/$', login_required(views.message_view),
        name='message'),

    url(r'^patient/problems/$', login_required(views.problems_view),
        name='problem_list'),
    url(r'^patient/problem/(?P<pk>[0-9]+)/$',
        login_required(views.problem_edit_view), name='problem_edit'),
    url(r'^patient/problems/new$', login_required(views.add_problem_view),
        name='problem_new'),

    url(r'^patient/allergies/$', login_required(views.allergies_view),
        name='allergy_list'),
    url(r'^patient/allergy/(?P<pk>[0-9]+)/$',
        login_required(views.allergy_edit_view), name='allergy_edit'),
    url(r'^patient/allergies/new$', login_required(views.add_allergy_view),
        name='allergy_new'),

    url(r'^api/problems/$', login_required(views.Problem_Index_View.as_view()),
        name='problem_index'),
    url(r'^api/problem/(?P<pk>[0-9]+)/$',
        login_required(views.ProblemView.as_view()), name='problem'),
    url(r'^api/allergies/$', login_required(views.Allergy_Index_View.as_view()),
        name='allergy_index'),
    url(r'^api/allergy/(?P<pk>[0-9]+)/$',
        login_required(views.AllergyView.as_view()), name='allergy'),

    # url(r'^api/doctor/(?P<pk>[0-9]+)/$', login_required(views.DoctorView.as_view()),
    #     name='doctor'),
]
