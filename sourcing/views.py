from django.shortcuts import render
from sourcing.models import Amazon, Ebay, Alibaba, Walmart
from beholder.eyeballs import amazon, ebay, walmart, target
import traceback

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
    rv = {
        'keywords': request.GET.get("keywords"),
        'walmartCatId': request.GET.get("walmartCatId"),
        'amazonCatId': request.GET.get("amazonCatId"),
        'ebayCatId': request.GET.get("ebayCatId"),
        'walmartPage': request.GET.get("walmartPage"),
        'amazonPage': request.GET.get("amazonPage"),
        'ebayPage': request.GET.get("ebayPage"),
        }

    context = {}
    context['pages'] = {
        'walmart': {
            'page': int(rv['walmartPage']),
            'prev': int(rv['walmartPage']) - 1,
            'next': int(rv['walmartPage']) + 1,
        },
        'amazon': {
            'page': int(rv['amazonPage']),
            'prev': int(rv['amazonPage']) - 1,
            'next': int(rv['amazonPage']) + 1,
        },
        'ebay': {
            'page': int(rv['ebayPage']),
            'prev': int(rv['ebayPage']) - 1,
            'next': int(rv['ebayPage']) + 1,
        }
    }

    specialQueries = {
        'Best Sellers': walmart.getBestSellers,
        'Clearance': walmart.getClearance,
        'Special_Buy': walmart.getSpecialBuy,
        'Trending': walmart.getTrending,
    }

    #  try to get amazon context data
    try:
        if rv["keywords"] in specialQueries:
            walmartItems = specialQueries[rv["keywords"]](
                walmartCatId=int(rv["amazonCatId"]))
            context['amazonItems'] = amazonItems

        else:
            amazonItems = amazon.search(
                keywords=rv["keywords"],
                amazonCatId=rv["amazonCatId"],
                amazonPage=rv["amazonPage"],
            )
            context['amazonItems'] = amazonItems

    except Exception as e:
        print(traceback.format_exc())


    #  try to get ebay context data
    try:
        if rv["keywords"] in specialQueries:
            walmartItems = specialQueries[rv["keywords"]](
                walmartCatId=int(rv["ebayCatId"]))
            context['ebayItems'] = ebayItems

        else:
            ebayItems = ebay.search(
                keywords=rv["keywords"],
                ebayCatId=rv["ebayCatId"],
                ebayPage=rv["ebayPage"],
            )
            context['ebayItems'] = ebayItems

    except Exception as e:
        print(traceback.format_exc())

    #  try to get walmart context data
    try:
        if rv["keywords"] in specialQueries:
            walmartItems = specialQueries[rv["keywords"]](
                walmartCatId=rv["walmartCatId"])
            context['walmartItems'] = walmartItems

        else:
            if bool(rv["walmartCatId"]) == True:
                walmartItems = walmart.search(
                    keywords=rv["keywords"],
                    walmartCatId=rv["walmartCatId"],
                    walmartPage=rv["walmartPage"],
                )
                context['walmartItems'] = walmartItems

    except Exception as e:
        print(traceback.format_exc())

    for key, value in context.items():
        if "Items" in key:
            context["active"] = str(key)
            break

    return render(request, 'sourcing/response.html', context)


"""
Scratchpad / Testing
"""
s = "one two three"
c = "There are two dogs."
