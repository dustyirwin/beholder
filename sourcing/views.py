from django.shortcuts import render
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

#  special queries for markets

meta_data['categories'] = dict(
    [(market, eyeball.categories) for market, eyeball in meta_data['eyeballs'].items()]
)

meta_data['specialQueries'] = {
    'walmart': {
        'Best Sellers': meta_data['eyeballs']["walmart"].getBestSellers,
        'Clearance': meta_data['eyeballs']["walmart"].getClearance,
        'Special_Buy': meta_data['eyeballs']["walmart"].getSpecialBuy,
        'Trending': meta_data['eyeballs']["walmart"].getTrending,
    },
    'amazon': {
    },
    'ebay': {
    }
}


def query(request, **kwargs):
    global meta_data
    context = {

        'categories': dict(
            [(market, eyeball.categories)
                for market, eyeball in meta_data['eyeballs'].items()]
        ),
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

    return render(request, 'sourcing/query.html', context)


def response(request, **kwargs):
    global meta_data

    default_pages = dict([(marketName+"Page", 1) for marketName in meta_data["eyeballs"].keys()])
    resp_vars = dict([(key, value) for key, value in request.GET.items()])
    resp_vars = {**default_pages, **resp_vars}

    #  try to get marketplace context data

    context = {'markets': [], }

    for key, value in resp_vars.items():

        if "CatId" in key and key[:-5] in meta_data["specialQueries"] and resp_vars["keywords"] in meta_data["specialQueries"][key[:-5]]:

            try:
                context['markets'].append(
                    {
                        "items": meta_data["specialQueries"][key[:-5]][resp_vars["keywords"]](
                            keywords=resp_vars["keywords"],
                            category=value,
                            page=resp_vars[key[:-5]+"Page"],
                        ),
                        "name": key[:-5],
                        "page": resp_vars[key[:-5]+"Page"],
                        "category": resp_vars[key[:-5]+"CatId"]
                    }
                )
            except Exception:
                print(traceback.format_exc())  # output error to std

        elif "CatId" in key and bool(value):
            try:
                context['markets'].append(
                    {
                        "items": meta_data["eyeballs"][key[:-5]].search(
                            keywords=resp_vars["keywords"],
                            category=value,
                            page=resp_vars[key[:-5]+"Page"],
                            ),
                        "name": key[:-5],
                        "page": resp_vars[key[:-5]+"Page"],
                        "category": resp_vars[key[:-5]+"CatId"]
                    }
                )
            except Exception:
                print(traceback.format_exc())  # output error to std

    #  try to get marketplace context data
    context = {}

    for key, value in resp_vars.items():
        if "CatId" in key and key[:-5] in meta_data["specialQueries"] and resp_vars["keywords"] in meta_data["specialQueries"][key[:-5]]:
            context[key[:-5]+"Items"] = meta_data["specialQueries"][key[:-5]][resp_vars["keywords"]](
                keywords=resp_vars["keywords"],
                category=value,
                page=resp_vars[key[:-5]+"Page"],
            )
        elif "CatId" in key and bool(value):
            context[key[:-5]+"Items"] = meta_data["eyeballs"][key[:-5]].search(
                keywords=resp_vars["keywords"],
                category=value,
                page=resp_vars[key[:-5]+"Page"]
            )
        else:
            continue

    return render(request, 'sourcing/response.html', context)


"""
Scratchpad / Testing


names = ["foo", "bar"]
tags = ["boz", "baz"]

varNames = [ k + j for k in names for j in tags ]
varNames

d = dict([("a",1),("b",2)]+[("d",1),("c",2)])
"""
