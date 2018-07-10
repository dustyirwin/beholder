from django.shortcuts import render, redirect
from inventory.models import ItemData
from beholder.eyeballs import session
from beholder.eyeballs import Eyes
# import traceback


def query(request):
    return render(request, 'search/query.html', context={'session': session.data})


def response(request):
    kwargs = {
        **{key[:-5]+'Page': '1' for key, value in request.GET.dict().items() if 'CatId' in key},
        **request.GET.dict()}

    if 'capture' in kwargs and 'market' in kwargs:

        for item in session.data['market_data'][kwargs['market']]['objects']:

            if str(kwargs['capture']) == str(item['item_id']):

                if ItemData.objects.filter(item_id=kwargs['capture']).exists():
                    session.data['item'] = {'item_id': kwargs['capture'], 'market': kwargs['market']}
                    session.save()
                    return redirect('inventory:itemDetails')

                else:
                    item = Eyes[kwargs['market']].getItemDetails(item, item_id=kwargs['capture'])
                    ItemData(
                        item_id=kwargs['capture'],
                        name=item['name'],
                        data=item, ).save()
                    session.data['item'] = item
                    session.save()
                    return redirect('inventory:itemDetails')

    # query marketplace for context data
    for market_name, market in Eyes.items():
        if market_name+'SE' in kwargs:
            session.data['market_data'][market_name]['search_enabled'] = kwargs[market_name+"SE"]
            session.save()
        if market_name+'SE' in kwargs and bool(kwargs[market_name+'SE']):
            market.findItems(**kwargs)

    session.data['active'] = session.data['active'] if 'active' not in kwargs else kwargs['active']
    session.data['kwargs'] = kwargs
    session.save()

    # construct context from item_ids
    for market_name, market in Eyes.items():
        if 'item_ids' in session.data['market_data'][market_name]:
            item_ids = session.data['market_data'][market_name]['item_ids']
            objects = [ItemData.objects.get(item_id=item_id).data for item_id in item_ids]
            session.data['market_data'][market_name]['objects'] = objects
        else:
            session.data['market_data'][market_name]['objects'] = None

    return render(request, 'search/response.html', context={'session': session.data})
