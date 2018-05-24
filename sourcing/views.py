from django.shortcuts import render
from .models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon, ebay, walmart, alibaba


ebay = ebay.ebayAPI()
amazon = amazon.amazonAPI()
walmart = walmart.walmartAPI()
alibaba = alibaba.alibabaAPI()

marketNames = ['walmart','ebay','amazon','alibaba']


def query(request):
    context = {
    'amazonCategories': amazon.categories,
    'ebayCategories': ebay.categories,
    'walmartCategories': walmart.categories,
    'alibabaCategories': alibaba.categories,
    'marketNames': marketNames,
    }
    return render(request, 'sourcing/query.html', context)


def response(request):
    amazonItems = amazon.search(request, Amazon)
    ebayItems = ebay.search(request, Ebay)
    #walMartItem = walmart.getItemInfo(request)

    context = {
        'amazonItems': amazonItem,
        #'walMartItems': walMartItem,
        'ebayItems': ebayItems,
    }
    return render(request, 'sourcing/response.html', context)
