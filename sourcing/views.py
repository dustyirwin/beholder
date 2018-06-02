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
    #wally.meta_data['categories'],
    #_eyeballs['ebay'].meta_data,
    #_eyeballs['amazon'].meta_data,
    ]

_eyeballs["walmart"].categories

def query(request, **kwargs):
    global meta_datas
    return render(request, 'sourcing/query.html', context = {"markets": meta_datas})


def response(request, **kwargs):
    global meta_data
    default_pages = dict(
        [(market+"Page", 1) for market in meta_data["eyeballs"].keys()])
    resp_vars = dict([(key, value) for key, value in request.GET.items()])
    resp_vars = {**default_pages, **resp_vars}

    #  query marketplace for context data

    code = "CatId"
    code_len = len(code)
    context = {
        'markets': [],
    }

    for key, value in resp_vars.items():

        if code in key and key[:-code_len] in meta_data["specialQueries"] and resp_vars["keywords"] in meta_data["specialQueries"][key[:-code_len]]:

            try:
                context['markets'].append(
                    {
                        "items": meta_data["specialQueries"][key[:-code_len]][resp_vars["keywords"]](
                            keywords=resp_vars["keywords"],
                            category=value,
                            page=resp_vars[key[:-code_len]+"Page"],
                        ),
                        "name": key[:-code_len],
                        "page": resp_vars[key[:-code_len]+"Page"],
                        "category": resp_vars[key[:-code_len]+code],
                        "active": True if resp_vars["active"] and resp_vars["active"] == key[:-code_len] else False,
                    }
                )
            except Exception:
                print(traceback.format_exc())  # output error to std

        elif code in key and bool(value):
            try:
                context['markets'].append(
                    {
                        "items": meta_data["eyeballs"][key[:-code_len]].search(
                            keywords=resp_vars["keywords"],
                            category=value,
                            page=resp_vars[key[:-code_len]+"Page"],
                            ),
                        "name": key[:-code_len],
                        "page": resp_vars[key[:-code_len]+"Page"],
                        "category": resp_vars[key[:-code_len]+code],
                        "active": True if resp_vars["active"] and resp_vars["active"] == key[:-code_len] else False,
                    }
                )
            except Exception:
                print(traceback.format_exc())  # output error to std

    context["marketNames"] = [market['name'] for market in context["markets"]]
    print(context["marketNames"])  # debugging

    return render(request, 'sourcing/response.html', context)
