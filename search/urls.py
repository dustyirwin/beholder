from django.conf.urls import url
from . import views

app_name = 'search'

urlpatterns = [
    url(r'^$', views.query, name='query'),
    url(r'^r/$', views.response, name='response'),
]
