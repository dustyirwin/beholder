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
        amazonItems = amazon.search(
            keywords=request.GET.get("keywords"),
            amazonCatId=request.GET.get("amazonCatId"),
            page=request.GET.get("page"),
        )
        context['amazonItems'] = amazonItems


    if request.GET.get("ebayCatId"):
        ebayItems = ebay.search(
            keywords=request.GET.get("keywords"),
            ebayCatId=request.GET.get("ebayCatId"),
            page=request.GET.get("page"),
        )
        context['ebayItems'] = ebayItems


    if request.GET.get("walmartCatId") and request.GET.get("keywords") in walmartQueries:
        walmartItems = walmartQueries[request.GET.get("keywords")]
        #ebaySalesData = ebay.getSalesData(walmartItems, Ebay=Ebay)
        context['walmartItems'] = walmartItems
    else:
        walmartItems = walmart.search(
            request,
            keywords=request.GET.get("keywords"),
            walmartCatId=request.GET.get("walmartCatId"),
            page=request.GET.get("page")
        )
        context['walmartItems'] = walmartItems

    return render(request, 'sourcing/response.html', context)
