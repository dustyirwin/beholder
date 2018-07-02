from django.shortcuts import render, redirect
from .models import ItemData
from beholder.eyeballs import session
from beholder.eyeballs import Eyes


def itemsList(request):
    kwargs = request.GET.dict()

    if 'item_id' in kwargs:
        session.data['item'] = ItemData.objects.get(item_id=kwargs['item_id'])
        session.save()
        return redirect('inventory:itemDetails')
    else:
        session.data['Inventory'] = {obj.item_id: obj.data for obj in ItemData.objects.all()[:19]}
        session.save()
        return render(request, 'inventory/home.html', context={'session': session.data})


def itemDetails(request, item_id=''):
    kwargs = request.GET.dict()

    if 'note' in kwargs:
        if bool(kwargs['note']):
            item = ItemData.objects.get(item_id=kwargs['item_id']) if 'item_id' in kwargs else ItemData.objects.get(item_id=kwargs['get_prices'])
            item.data['notes'].append(kwargs['note'])
            item.save()

    if 'get_prices' in kwargs and 'query' in kwargs:
        kwargs['keywords'] = kwargs['query']
        Eyes['ebay'].getItemPriceHistories(**kwargs)

    session.data['item'] = ItemData.objects.get(item_id=item_id if 'get_prices' not in kwargs else kwargs['get_prices']).data
    session.save()
    return render(request, 'inventory/details.html', context={'session': session.data})
