from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    url(r'^details/$', views.ItemDetailsView.as_view(), name='details'),
    url(r'^$', views.ItemListView.as_view(), name='itemList'),
]
