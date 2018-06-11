from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^details/$', views.ItemDetails.as_view(), name='itemDetails'),
    url(r'^$', views.ItemList.as_view(), name='itemList'),
]
