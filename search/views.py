from django.shortcuts import render
from beholder.eyeballs import eyeballs
# import traceback

# create meta data for html page context
markets = [eyeballs[market].market for market in eyeballs.keys()]

specialQueries = {
    'Best Sellers': eyeballs['walmart'].getBestSellers,
    'Clearance': eyeballs['walmart'].getClearance,
    'Special Buy': eyeballs['walmart'].getSpecialBuy,
    'Trending': eyeballs['walmart'].getTrending, }


def query(request):
    global markets
    return render(
        request, 'search/query.html', context={"markets": markets})


def response(request):
    global markets
    global specialQueries
    kwargs = request.GET.dict()

    #  query marketplace for context data
    for sqk in specialQueries.keys():

        if sqk in kwargs['keywords']:
            specialQueries[kwargs["keywords"]](**kwargs)

    for key, value in kwargs.items():

        if 'CatId' in key:
            eyeballs[key[:-5]].search(**kwargs)
            break

    pages = {key[:-5]+"Page": 1 for key in request.GET.dict().keys() if 'CatId' in key}
    kwargs = {**pages, **kwargs}
    context = {**{'markets': markets}, **kwargs}
    context["marketNames"] = [market['name'] for market in context["markets"]]
    context["active"] = context['markets'][0]['name'] if 'active' not in kwargs else kwargs['active']

    return render(request, 'search/response.html', context)
