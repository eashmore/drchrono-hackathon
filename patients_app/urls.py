from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'patients_app'

urlpatterns = [
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^accounts/oauth/$', views.oauth_view, name='oauth'),
    url(r'^accounts/logout/$', login_required(views.logout_view), name='logout'),
    url(r'^$', login_required(views.home_view), name='home'),
    url(r'^patient/$', login_required(views.patient_view), name='patient_edit'),
    url(r'^patient/logout$', login_required(views.patient_logout), name='patient_logout'),
    url(r'^patient/problems$', login_required(views.problems_view), name='problem_list'),


    url(r'^patient/(?P<pk>[0-9]+)/$', login_required(views.PatientView.as_view()),
        name='patient'),

    # url(r'^api/doctor/(?P<pk>[0-9]+)/$', login_required(views.DoctorView.as_view()),
    #     name='doctor'),
]
