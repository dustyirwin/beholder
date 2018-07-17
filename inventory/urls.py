from django.conf.urls import url
from . import views

app_name = 'inventory'


#  regex for item_id ~ ^(?P<item_id>[a-zA-Z0-9]+)$'
urlpatterns = [
    url(r'^details/(?P<item_id>.+)/$', views.itemDetails, name='details'),
    url(r'^details/$', views.itemDetails, name='details'),
    url(r'^$', views.IndexView.as_view(), name='home'), ]
