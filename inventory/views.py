from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from beholder.eyeballs import Ebay
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

        else:
            return get_object_or_404(ItemData.objects.filter(item_id=kwargs['item_id']))
