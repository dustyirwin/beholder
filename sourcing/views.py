from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404
from django.views.generic import DetailView, ListView
from pricing.models import *
import mws

def index(request):
    products_api = mws.Products(access_key='AKIAJGZE5C5XUOCSORYQ',
                                secret_key='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',
                                account_id='A3A3KAZ6LDQG83',
                                )
    products = products_api.get_lowest_offer_listings_for_asin('US','B00009WAU9')
    print(products.parsed)
    return render(request,'sourcing/index.html')