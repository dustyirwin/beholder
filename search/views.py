from django.shortcuts import render, redirect
from inventory.models import ItemData
from login.models import SessionData
from beholder.eyeballs import Eyes
import asyncio
# import traceback


def query(request):
    session = SessionData.objects.get(user=request.user)
    return render(request, 'search/query.html', context={'session': session.data})

def response(request):
    session = SessionData.objects.get(user=request.user)
    kwargs = {
        **{key[:-5]+'Page': '1' for key, value in request.GET.dict().items() if 'CatId' in key},
        **request.GET.dict()}
    kwargs['user'] = session.user

    # gather additional details, capture item to db, and redirect to inventory:ItemDetails
    if 'capture' in kwargs and 'market' in kwargs:
        item = ItemData.objects.get(item_id=kwargs['capture']).data
        item = Eyes[kwargs['market']].getItemDetails(item, item_id=kwargs['capture'])
        session.data['item'] = item
        session.save()
        return redirect('inventory:itemDetails')

    # activate user-requested marketplaces and query
    kwargs['market_names'] = [k[:-2] for k in kwargs if 'SE' in k and bool(k)]
    Eyes['center'].search(**kwargs)

    session.data['active'] = session.data['active'] if 'active' not in kwargs else kwargs['active']
    session.data['kwargs'] = kwargs
    session.save()

    # construct context from item_ids
    for market_name, market in session.data['market_data'].items():

        if 'item_ids' in session.data['market_data'][market_name]:
            item_ids = session.data['market_data'][market_name]['item_ids']
            objects = [ItemData.objects.get(item_id=item_id).data for item_id in item_ids]
            session.data['market_data'][market_name]['objects'] = objects

        else:
            session.data['market_data'][market_name]['objects'] = None

    return render(request, 'search/response.html', context={'session': session.data})
