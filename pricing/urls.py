from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'pricing'

urlpatterns = [
    url(r'^$', views.ebay, name='index'),

    url(r'^ebay/$', views.ebay, name='ebay'),
    url(r'^ebay/search/$', views.searchEbay, name='searchEbay'),

    url(r'^amazon/$', views.amazon, name='amazon'),
    url(r'^amazon/search/$', views.searchAmazon, name='searchAmazon'),

    url(r'^alibaba/$', views.amazon, name='alibaba'),
    url(r'^alibaba/search/$', views.searchAmazon, name='searchAlibaba'),

    url(r'^priceEbayItem/$', views.priceEbayItem, name='priceEbayItem'),
    url(r'^priceAmazonItem/$', views.searchAmazon, name='findASIN'),
]
