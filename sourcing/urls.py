from django.conf.urls import url
from . import views

app_name = 'sourcing'

urlpatterns = [
    url(r'^q/$', views.query, name='query'),
    url(r'^q/r/$', views.response, name='response'),
]
