from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='login'),
    url(r'^welcome/$', views.IndexView.as_view(), name='landing'),
]
