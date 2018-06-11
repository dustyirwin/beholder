from django.shortcuts import render
from beholder.eyeballs import eyeballs
# import traceback

# create meta data for html page context
meta_datas = [eyeballs[market].meta_data for market in eyeballs.keys()]

specialQueries = {
    'Best Sellers': eyeballs['walmart'].getBestSellers,
    'Clearance': eyeballs['walmart'].getClearance,
    'Special Buy': eyeballs['walmart'].getSpecialBuy,
    'Trending': eyeballs['walmart'].getTrending, }


def query(request, **kwargs):
    global meta_datas

    return render(
        request, 'search/query.html', context={"markets": meta_datas})


def response(request, **kwargs):
    global meta_datas
    resp_vars = dict([(key, value) for key, value in request.GET.items()])
    default_pages = dict(
        [(key[:-5]+"Page", 1) for key, value in resp_vars.items(
        ) if "CatId" in key or value == 'All'])
    resp_vars = {**resp_vars, **default_pages}

    #  query marketplace for context data
    code = "CatId"
    code_len = len(code)
    context = {**{'markets': meta_datas}, **resp_vars}

    for market in context['markets']:

        for key, value in resp_vars.items():

            if code in key and resp_vars['keywords'] in specialQueries.keys():
                specialQueries[resp_vars["keywords"]](**resp_vars)

            elif code in key and bool(value):
                eyeballs[key[:-code_len]].search(**resp_vars)

    context["marketNames"] = [market['name'] for market in context["markets"]]
    context["active"] = context['markets'][0][
        'name'] if 'active' not in resp_vars else resp_vars['active']

    return render(request, 'search/response.html', context)
