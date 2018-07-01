from django.conf.urls import url
from . import views

app_name = 'inventory'


#  regex for item_id ~ ^(?P<item_id>[a-zA-Z0-9]+)$'
urlpatterns = [
    url(r'^details/(?P<item_id>.+)/$', views.ItemDetails.as_view(), name='ItemDetails'),
    url(r'^details/$', views.ItemDetails.as_view(), name='ItemDetails'),
    url(r'^$', views.itemsList, name='itemsList'), ]
