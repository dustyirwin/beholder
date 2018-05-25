from django.shortcuts import render
from .models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon, ebay, walmart, target


ebay = ebay.ebayAPI()
amazon = amazon.amazonAPI()
walmart = walmart.walmartAPI()
target = target.targetAPI()

marketNames = ['walmart','ebay','amazon','target']

def query(request):
    context = {
    'amazonCategories': amazon.categories,
    'ebayCategories': ebay.categories,
    'walmartCategories': walmart.categories,
    'targetCategories': target.categories,
    'marketNames': marketNames,
    }
    return render(request, 'sourcing/query.html', context)


def response(request):
    context = {}
    walmartQueries = {
        'Best Sellers': walmart.getBestSellers(request, Walmart),
        'Clearance': walmart.getClearance(request, Walmart),
        'Special Buy': walmart.getSpecialBuy(request, Walmart),
        'Trending': walmart.getTrending(Walmart),
        }

    if request.GET.get("amazonCatId"):
        amazonItems = amazon.search(request, Amazon)
        context['amazonItems'] = amazonItems

    if request.GET.get("ebayCatId"):
        ebayItems = ebay.search(request, Ebay)
        context['ebayItems'] = ebayItems

    if request.GET.get("walmartCatId") and request.GET.get("keywords") in walmartQueries:
        walmartItems = walmartQueries[request.GET.get("keywords")]
        context['walmartItems'] = walmartItems
    else:
        walmartItems = walmart.search(request, Walmart)
        context['walmartItems'] = walmartItems

    return render(request, 'sourcing/response.html', context)
