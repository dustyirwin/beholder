from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from beholder.eyeballs import Ebay
from beholder.eyeballs import Eyes
from beholder.eyeballs import session
from .models import ItemData


class ItemList(ListView):
    template_name = 'inventory/home.html'
    context_object_name = 'items'
    ordering = ['id']

    def get_object(self):
        return ItemData.objects.all()


class ItemDetails(DetailView):
    template_name = 'inventory/details.html'
    context_object_name = 'item'

    def get_object(self):
        kwargs = self.request.GET.dict()
        if kwargs.get('note'):
            if bool(kwargs['note']):
                item = ItemData.objects.get(item_id=kwargs['item_id']) if 'item_id' in kwargs else ItemData.objects.get(item_id=kwargs['get_prices'])
                item.data['notes'].append(kwargs['note'])
                item.save()

        if 'get_prices' in kwargs and 'query' in kwargs:
            kwargs['keywords'] = kwargs['query']
            Ebay.getPriceHistories(**kwargs)
            return ItemData.objects.get(item_id=kwargs['get_prices'])

        elif 'capture' in session.data.keys():
            return get_object_or_404(ItemData.objects.filter(item_id=session.data['capture']['item_id']))
        else:
            return get_object_or_404(ItemData.objects.filter(item_id=kwargs['item_id']))
