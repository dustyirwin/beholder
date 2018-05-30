from django.shortcuts import render
from sourcing.models import Amazon, Ebay, Walmart
from beholder.eyeballs import amazon, ebay, walmart
import traceback


#  instantiate eyeballs into meta_data
meta_data = {
    'eyeballs': {
        "walmart": walmart.walmartEye(),
        "amazon": amazon.amazonEye(),
        "ebay": ebay.ebayEye(),
    },
}

#  special queries for markets
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

    context['marketNames'] = [market['name'] for market in context['markets']]
    if "active" in resp_vars:
        context["active"] = resp_vars["active"]
    else:
        context["active"] = context['marketNames'][0]

    #  debugging
    print('context.keys(): ', context.keys())
    print('marketNames: ', context['marketNames'])
    print('active: ', context["active"])
    #  debugging

    return render(request, 'sourcing/response.html', context)


"""
Scratchpad / Testing
"""
