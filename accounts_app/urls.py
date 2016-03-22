from django.conf.urls import url

from . import views

app_name = 'account_app'

urlpatterns = [
    url(r'login/$', views.login_view, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
]
