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
        'Best Sellers': walmart.getBestSellers(request),
        'Clearance': walmart.getClearance(request),
        'Special Buy': walmart.getSpecialBuy(request),
        'Trending': walmart.getTrending(),
        }

    if request.GET.get("amazonCatId"):
        amazonItems = amazon.search(request, Amazon=Amazon)
        context['amazonItems'] = amazonItems
        context['amazonItems']['marketName'] = "amazon"

    if request.GET.get("ebayCatId"):
        ebayItems = ebay.search(request, Ebay=Ebay)
        context['ebayItems'] = ebayItems
        context['ebayItems']['marketName'] = "ebay"

    if request.GET.get("walmartCatId") and request.GET.get("keywords") in walmartQueries:
        walmartItems = walmartQueries[request.GET.get("keywords")]
        ebaySalesData = ebay.getSalesData(walmartItems, Ebay=Ebay)
        context['walmartItems'] = walmartItems
        context['walmartItems']['marketName'] = "walmart"
    else:
        walmartItems = walmart.search(request, Walmart=Walmart)
        context['walmartItems'] = walmartItems

    return render(request, 'sourcing/response.html', context)
