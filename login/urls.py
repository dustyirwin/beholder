from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^landing$', views.landing, name='landing'),
]
