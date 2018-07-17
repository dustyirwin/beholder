from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from datetime import datetime
from .models import ItemData
from search.forms import SearchForm
from login.models import SessionData
from beholder.eyeballs import Eyes


class IndexView(TemplateView):
    template_name = 'inventory/home.html'

    def get(self, request):
        kwargs = request.GET.dict()

        if 'item_id' in kwargs:
            return redirect('inventory:details', item_id=kwargs['item_id'])

        else:
            recent_items = ItemData.objects.all()[:20]
            return render(request, 'inventory/home.html', {'recent_items': recent_items})


def itemDetails(request, item_id=''):
    kwargs = request.GET.dict()
    session = SessionData.objects.get(user=request.user)
    if 'note' in kwargs:

        if bool(kwargs['note']):
            item = ItemData.objects.get(item_id=kwargs['item_id']) if 'item_id' in kwargs else ItemData.objects.get(item_id=kwargs['get_prices'])
            item.data['notes'][datetime.now().__str__()[:19]] = {
                'note': kwargs['note'],
                'user': 'dusty', }
            item.save()

    if 'get_prices' in kwargs and 'query' in kwargs:
        kwargs['keywords'] = kwargs['query']
        Eyes['ebay'].getItemPrices(**kwargs)
        session.data['item'] = ItemData.objects.get(item_id=kwargs['get_prices']).data
        session.save()

    if bool(item_id):
        session.data['item'] = ItemData.objects.get(item_id=item_id).data
        session.save()

    return render(request, 'inventory/details.html', context={'session': session.data})
