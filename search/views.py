from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from inventory.models import ItemData
from login.models import SessionData
from beholder.eyeballs import Eye
import asyncio
# import traceback


class IndexView(TemplateView):
    template_name = 'search/query.html'
    eye = Eye()

    def get(self, request):
        session = self.eye.open(request.user)
        return render(request, 'search/query.html', {'session': session.data})

    def post(self, request):
        session = eye.open(request.user)

        recent_items = ItemData.objects.all()[:20]
        return redirect('inventory:home')


def response(request):
    session = Center.open(request.user)

    # gather additional details, capture item to db, and redirect to inventory:ItemDetails
    if 'capture' in kwargs and 'market' in kwargs:
        item = ItemData.objects.get(item_id=kwargs['capture']).data
        item = Eyes[kwargs['market']].getItemDetails(item, item_id=kwargs['capture'])
        item.save()
        return redirect('inventory:details', item_id=kwargs['capture'])

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
