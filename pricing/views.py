from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404
#from django.views.generic import DetailView, ListView
#from django.core.paginator import Paginator
#from datetime import datetime
from .models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon as az
from beholder.eyeballs import ebay as eb
from beholder.eyeballs import walmart as wm


def amazon(request):
    return render(request, 'pricing/amazon.html')


def searchAmazon(request):
    amazon = az.amazonAPI()
    amazonItems = amazon.search(request, Amazon)
    # if pricing an eBay item, insert ebayItem into context
    if request.GET.get('itemId'):
        ebayItem = Ebay.objects.get(itemId=request.GET.get('itemId'))
        return render(request, 'pricing/amazon.html', {
                'items': amazonItems,
                'ebayItem': ebayItem})
    else:
        return render(request, 'pricing/amazon.html', {'items': amazonItems})

def ebay(request):
    return render(request, 'pricing/ebay.html')

def searchEbay(request):
    ebay = eb.ebayAPI()
    ebayItems = ebay.search(request, Ebay)

    return render(request, 'pricing/ebay.html', ebayItems)

def priceEbayItem(request):
    ebay = eb.ebayAPI()
    context = ebay.price(request, Ebay, Amazon)
    return render(request, 'pricing/priceEbayItem.html', context)

def sourceItem(request):
    ebay = eb.ebayAPI()
    amazon = az.amazonAPI()
    walmart = wm.walmartAPI()
    amazonItem = amazon.scrape(request, Amazon)
    ebayItems = ebay.getUPC(request, )
    walMartItem = walmart.getItemInfo(request)
    context = {
        'amazonItem': amazonItem,
        'walMartItem': walMartItem,
        'ebayItems': ebayItems,
    }
    return render(request, 'pricing/sourceItem.html', context)
