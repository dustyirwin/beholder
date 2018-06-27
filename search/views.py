from django.shortcuts import render, redirect
from inventory.models import ItemData
from beholder.eyeballs import Eyes
from beholder.eyeballs import session
# import traceback


def query(request):
    return render(
        request, 'search/query.html', context={
            'markets': [market for name, market in session.data['markets'].items()]})


def response(request):
    kwargs = {
        **{key[:-5]+'Page': '1' for key, value in request.GET.dict().items() if 'CatId' in key},
        **request.GET.dict()}

    if 'capture' in kwargs and 'market' in kwargs:

        for item in session.data['markets'][kwargs['market']]['items']:

            if str(kwargs['capture']) == str(item['item_id']):
                if ItemData.objects.filter(item_id=kwargs['capture']).exists():
                    session.data['capture'] = {'item_id': kwargs['capture'], 'market': kwargs['market']}
                    session.save()
                    return redirect('inventory:itemDetails')
                else:
                    item = Eyes[kwargs['market']].getItemDetails(item, item_id=kwargs['capture'])
                    item['market'] = kwargs['market']
                    ItemData(
                        item_id=kwargs['capture'],
                        name=item['name'],
                        data=item).save()
                    session.data['capture'] = {'item_id': kwargs['capture'], 'market': kwargs['market']}
                    session.save()
                    return redirect('inventory:itemDetails')

    #  query marketplace for context data
    for _, market in Eyes.items():
        market.findItems(**kwargs)

    context = {'markets': [market for name, market in session.data['markets'].items()]}
    context['market_names'] = session.data['market_names']
    context['active'] = session.data['active'] if 'active' not in kwargs else kwargs['active']

    return render(request, 'search/response.html', context=context)
