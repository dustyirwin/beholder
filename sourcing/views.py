from django.shortcuts import render, Http404
from sourcing.models import Amazon, Ebay, Walmart
from beholder.eyeballs import amazon, ebay, walmart
import traceback


#  instantiate Eyes into _eyeballs dict
meta_data = {
    'eyeballs': {
        "walmart": walmart.walmartEye(),
        "amazon": amazon.amazonEye(),
        "ebay": ebay.ebayEye(),
    },
}
meta_data['categories'] = dict(
    [ (market, eyeball.categories) for market, eyeball in meta_data['eyeballs'].items() ]
)
meta_data['specialQueries'] = {
    'walmart': {
        'Best Sellers': meta_data['eyeballs']["walmart"].getBestSellers,
        'Clearance': meta_data['eyeballs']["walmart"].getClearance,
        'Special_Buy': meta_data['eyeballs']["walmart"].getSpecialBuy,
        'Trending': meta_data['eyeballs']["walmart"].getTrending,
    }
}


def query(request, **kwargs):
    global meta_data
    context = {
        'options': {
            'walmart': {
                "FreeShippingOnly": True,
            },
            'amazon': {
                "AutoScrape": False,
                "New Items Only": True,
            },
            'ebay': {
                "BuyItNowOnly": True,
            },
        },
    }
    return render(request, 'sourcing/query.html', meta_data)


def response(request, **kwargs):
    global meta_data
    default_pages = dict([ (marketName+"Page", 1) for marketName in meta_data["eyeballs"].keys()])
    resp_vars = dict([ (key, value) for key, value in request.GET.items() ])
    resp_vars = {**default_pages, **resp_vars}

    #  try to get marketplace context data
    context = dict(
        [ ("active", key[:-5]+"Items") for key, value in resp_vars.items() if "CatId" in key ]
    )

    for key, value in resp_vars.items():
        if "CatId" in key and key[:-5] in meta_data["specialQueries"] and resp_vars["keywords"] in meta_data["specialQueries"][key[:-5]]:
            try:
                context[key[:-5]+"Items"] = meta_data["specialQueries"][key[:-5]][resp_vars["keywords"]](
                    keywords=resp_vars["keywords"],
                    category=value,
                    page=resp_vars[key[:-5]+"Page"],
                    )
            except:
                print(traceback.format_exc()) #  output error to std

        elif "CatId" in key and bool(value):
            try:
                context[key[:-5]+"Items"] = meta_data["eyeballs"][key[:-5]].search(
                    keywords=resp_vars["keywords"],
                    category=value,
                    page=resp_vars[key[:-5]+"Page"]
                )
            except:
                print(traceback.format_exc())  # output error to std

        else:
            continue

    return render(request, 'sourcing/response.html', context)


"""
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
                ebayPage=context['pages']['ebayPage']
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
                    walmartPage=context['pages']['walmartPage']
                )
                context['walmartItems'] = walmartItems

    except Exception as e:
        print(traceback.format_exc())
"""

"""
Scratchpad / Testing
"""

names = ["foo", "bar"]
tags = ["boz", "baz"]

varNames = [ k + j for k in names for j in tags ]
varNames

d = dict([("a",1),("b",2)]+[("d",1),("c",2)])
