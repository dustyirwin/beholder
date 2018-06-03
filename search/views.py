from django.shortcuts import render
from search.models import ItemData
from beholder.eyeballs import Walmart, Ebay, Amazon
import traceback

#  instantiate market objects into eyeballs dict
eyeballs = {
    "walmart": Walmart(),
    "ebay": Ebay(),
    #"amazon": Amazon(),
    }

# create meta data for html page context
meta_datas = [eyeballs[market].meta_data for market in eyeballs.keys()]

specialQueries = {
    'Best Sellers': eyeballs['walmart'].getBestSellers,
    'Clearance': eyeballs['walmart'].getClearance,
    'Special Buy': eyeballs['walmart'].getSpecialBuy,
    'Trending': eyeballs['walmart'].getTrending, }

def query(request, **kwargs):
    global meta_datas

    return render(request, 'search/query.html', context = {"markets": meta_datas})

def response(request, **kwargs):
    global meta_datas
    resp_vars = dict([(key, value) for key, value in request.GET.items()])
    default_pages = dict(
        [(key[:-5]+"Page", 1) for key, value in resp_vars.items() if "CatId" in key or value == 'All'])
    resp_vars = {**resp_vars, **default_pages}

    #  query marketplace for context data
    code = "CatId"
    code_len = len(code)
    context = {**{'items': []}, **{'markets': meta_datas}, **resp_vars}

    for key, value in resp_vars.items():

        if code in key and resp_vars['keywords'] in specialQueries.keys():
            context['items'].append({
                "items": specialQueries[resp_vars["keywords"]](**resp_vars),
                "name": key[:-code_len],
                "page": resp_vars[key[:-code_len]+"Page"],
                "category": resp_vars[key[:-code_len]+code],
                "active": True if "active" in resp_vars and resp_vars["active"] == key[:-code_len] else False,
            })

        elif code in key and bool(value):
            context['items'].append({
                "items": eyeballs[key[:-code_len]].search(**resp_vars),
                "name": key[:-code_len],
                "page": resp_vars[key[:-code_len]+"Page"],
                "category": resp_vars[key[:-code_len]+code],
                "active": True if "active" in resp_vars and resp_vars["active"] == key[:-code_len] else False,
                })

    context["marketNames"] = [market['name'] for market in context["markets"]]
    context['items'][0]['active'] = True
    print("context.keys(): ", context.keys())
    return render(request, 'search/response.html', context)

"""
resp_vars = {'keywords': 'stuff', 'walmartCatId': 12355, 'walmartPage': 1}
code_len = 5
contextz = {'items': []}
key = "walmartCatId"
value = 21344
contextz['items'].append({
    "items": eyeballs[key[:-code_len]].search(
        keywords=resp_vars["keywords"],category=value,page=resp_vars[key[:-code_len]+"Page"]),
    "name": key[:-code_len],
    "page": resp_vars[key[:-code_len]+"Page"],
    "category": resp_vars[key[:-code_len]+code],
    "active": True if resp_vars["active"] and resp_vars["active"] == key[:-code_len] else False,})
contextz
"""
