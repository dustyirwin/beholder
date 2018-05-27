from django.shortcuts import render
from sourcing.models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon, ebay, walmart, target


ebay = ebay.ebayEye()
amazon = amazon.amazonEye()
walmart = walmart.walmartEye()
#target = target.targetEye()

marketNames = ['walmart','ebay','amazon','target']

def query(request):
    context = {
    'amazonCategories': amazon.categories,
    'ebayCategories': ebay.categories,
    'walmartCategories': walmart.categories,
    #'targetCategories': target.categories,
    }
    return render(request, 'sourcing/query.html', context)


def response(request):
    context = {}

    walmartQueries = {
        'Best Sellers': walmart.getBestSellers,
        'Clearance': walmart.getClearance,
        'Special Buy': walmart.getSpecialBuy,
        'Trending': walmart.getTrending,
    }
    ebayQueries = {}
    amazonQueries = {}

    #  try to get amazon context data
    try:
        if bool(request.GET.get("amazonCatId")) == True:

            if request.GET.get("keywords") in walmartQueries or request.GET.get("keywords") in ebayQueries:
                pass
            else:
                amazonItems = amazon.search(
                    keywords=request.GET.get("keywords"),
                    amazonCatId=request.GET.get("amazonCatId"),
                    page=request.GET.get("page"),
                )
                context['amazonItems'] = amazonItems

    except Exception as e:
        print(e)

    #  try to get ebay context data
    try:
        if bool(request.GET.get("ebayCatId")) == True:

            if request.GET.get("keywords") in walmartQueries or request.GET.get("keywords") in amazonQueries:
                pass
            else:
                ebayItems = ebay.search(
                    keywords=request.GET.get("keywords"),
                    ebayCatId=request.GET.get("ebayCatId"),
                    page=request.GET.get("page"),
                )
                context['ebayItems'] = ebayItems

    except Exception as e:
        print(e)

    #  try to get walmart context data
    try:
        if request.GET.get("keywords") in walmartQueries:
            walmartItems = walmartQueries[request.GET.get("keywords")](
                walmartCatId=int(request.GET.get("walmartCatId")))
            context['walmartItems'] = walmartItems

        elif request.GET.get("keywords") in amazonQueries or request.GET.get("keywords") in ebayQueries:
            pass

        else:
            if bool(request.GET.get("walmartCatId")) == True:
                walmartItems = walmart.search(
                    keywords=request.GET.get("keywords"),
                    walmartCatId=request.GET.get("walmartCatId"),
                    page=request.GET.get("page")
                )
                context['walmartItems'] = walmartItems
    except Exception as e:
        print(e)

    return render(request, 'sourcing/response.html', context)


"""
Scratchpad / Testing


_walmart = walmart.walmartEye()
_walmartQueries = {
    'Best Sellers': _walmart.getBestSellers,
    'Clearance': _walmart.getClearance,
    'Special Buy': _walmart.getSpecialBuy,
    'Trending': _walmart.getTrending,}

type(_walmartQueries['Best Sellers'](walmartCatId=3944)) == list
import pdb; pdb.set_trace()
type(_walmartQueries['Clearance'](walmartCatId=3944)) == list
type(_walmartQueries['Special Buy'](walmartCatId=3944)) == list
type(_walmartQueries['Trending']()) == list
"""
