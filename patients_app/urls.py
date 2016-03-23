from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'patients_app'

urlpatterns = [
    url(r'accounts/login/$', views.login_view, name='login'),
    url(r'accounts/oauth/$', views.oauth_view, name='oauth'),
    url(r'accounts/logout/$', login_required(views.logout_view), name='logout'),
    url(r'^$', login_required(views.home_view), name='home'),
    url(r'(?P<pk>[0-9]+)/$', login_required(views.PatientView.as_view()),
        name='patient')
]
