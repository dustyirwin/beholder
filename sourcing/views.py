from django.shortcuts import render
from .models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon, ebay, walmart, alibaba


ebay = ebay.ebayAPI()
amazon = amazon.amazonAPI()
walmart = walmart.walmartAPI()
alibaba = alibaba.alibabaAPI()

marketNames = ['walmart','ebay','amazon','target']
walmartQueries = ['Best Sellers','Clearance','Special Buy','Trending']

def query(request):
    context = {
    'amazonCategories': amazon.categories,
    'ebayCategories': ebay.categories,
    'walmartCategories': walmart.categories,
    'alibabaCategories': target.categories,
    'marketNames': marketNames,
    }
    return render(request, 'sourcing/query.html', context)


def response(request):
    amazonItems = amazon.search(request, Amazon)
    ebayItems = ebay.search(request, Ebay)

    if request.GET.get("keywords") in walmartQueries:
        if request.GET.get("keywords") = walmartQueries[0]
            walMartItems = walmart.getBestSellers(request, Walmart)
    context = {
        'amazonItems': amazonItems,
        'walMartItems': walMartItems,
        'ebayItems': ebayItems,
    }
    return render(request, 'sourcing/response.html', context)
