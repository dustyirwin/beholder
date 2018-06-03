from django.shortcuts import render
from sourcing.models import ItemData
from beholder.eyeballs import Walmart, Ebay, Amazon
import traceback

#  instantiate market objects into _eyeballs dict
_eyeballs = {
    "walmart": Walmart(),
    "ebay": Ebay(),
    "amazon": Amazon(),
    }

# create meta data for html page context
meta_datas = [
    _eyeballs['walmart'].meta_data,
    _eyeballs['ebay'].meta_data,
    _eyeballs['amazon'].meta_data,
    ]

specialQueries = {
    'Best Sellers': _eyeballs['walmart'].getBestSellers,
    'Clearance': _eyeballs['walmart'].getClearance,
    'Special Buy': _eyeballs['walmart'].getSpecialBuy,
    'Trending': _eyeballs['walmart'].getTrending, }

def query(request, **kwargs):
    global meta_datas

    return render(request, 'sourcing/query.html', context = {"markets": meta_datas})

def response(request, **kwargs):
    global meta_datas
    resp_vars = dict([(key, value) for key, value in request.GET.items()])
    default_pages = dict(
        [(key[:-5]+"Page", 1) for key, value in resp_vars.items() if "CatId" in key or value == 'All'])
    resp_vars = {**default_pages, **resp_vars}

    #  query marketplace for context data
    code = "CatId"
    code_len = len(code)
    context = {**{'items': []}, **{'markets': meta_datas}}

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
                "items": _eyeballs[key[:-code_len]].search(**resp_vars),
                "name": key[:-code_len],
                "page": resp_vars[key[:-code_len]+"Page"],
                "category": resp_vars[key[:-code_len]+code],
                "active": True if "active" in resp_vars and resp_vars["active"] == key[:-code_len] else False
                })

    context["marketNames"] = [market['name'] for market in context["markets"]]

    return render(request, 'sourcing/response.html', context)

"""
resp_vars = {'keywords': 'stuff', 'walmartCatId': 12355, 'walmartPage': 1}
code_len = 5
contextz = {'items': []}
key = "walmartCatId"
value = 21344
contextz['items'].append({
    "items": _eyeballs[key[:-code_len]].search(
        keywords=resp_vars["keywords"],category=value,page=resp_vars[key[:-code_len]+"Page"]),
    "name": key[:-code_len],
    "page": resp_vars[key[:-code_len]+"Page"],
    "category": resp_vars[key[:-code_len]+code],
    "active": True if resp_vars["active"] and resp_vars["active"] == key[:-code_len] else False,})
contextz
"""
