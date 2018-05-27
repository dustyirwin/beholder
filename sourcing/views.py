from django.shortcuts import render
from .models import Amazon, Ebay, Alibaba, Walmart
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
        'Best Sellers': walmart.getBestSellers(
            walmartCatId=request.GET.get("walmartCatId"),),
        'Clearance': walmart.getClearance(
            walmartCatId=request.GET.get("walmartCatId")),
        'Special Buy': walmart.getSpecialBuy(
            walmartCatId=request.GET.get("walmartCatId")),
        'Trending': walmart.getTrending(),
        }
    ebayQueries = {}
    amazonQueries = {}

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

    try:
        if request.GET.get("keywords") in walmartQueries:
            walmartItems = walmartQueries[request.GET.get("keywords")]
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
