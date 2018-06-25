from django.shortcuts import render, redirect
from inventory.models import ItemData
from search.models import SessionData
from beholder.eyeballs import eyeballs
# import traceback

# load session data
session = SessionData.objects.get(user='dusty')
# instantiate eyeballs into dict
Eyes = eyeballs()

def query(request):
    return render(request, 'search/query.html', context={"markets": session.data['markets']})


def response(request):
    kwargs = {
        **{key[:-5]+'Page': '1' for key, value in request.GET.dict().items() if 'CatId' in key},
        **request.GET.dict()}

    if 'capture' in kwargs and 'market' in kwargs:
        item = Eyes[kwargs['market']].getItemDetails(**kwargs)
        items = session.data[kwargs['market']]['items']
        for _item in items:
            if _item['item_id'] == kwargs['capture']:
                ItemData(
                    item_id=kwargs['capture'],
                    name=_item['name'],
                    data={**item, **_item}
                    ).save()
                return redirect('inventory:itemDetails', item_id=kwargs['capture'])

    #  query marketplace for context data
    for _, market in Eyes.items():
        market.findItems(**kwargs)

    context = {'markets': session.data['markets']}
    context['marketNames'] = [market['name'] for market in session.data['markets']]
    context['active'] = 'walmart' if 'active' not in kwargs else kwargs['active']

    return render(request, 'search/response.html', context)
