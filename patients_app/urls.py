from django.conf.urls import url

from . import views

app_name = 'account_app'

urlpatterns = [
    url(r'accounts/login/$', views.login_view, name='login'),
    url(r'accounts/oauth/$', views.oauth_view, name='oauth'),
    url(r'accounts/logout/$', views.logout_view, name='logout'),
]
