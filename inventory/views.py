from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from beholder.eyeballs import eyeballs
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
        if 'item_id' in kwargs and 'compare' in kwargs:
            eyeballs[kwargs['compare']].compare_item(**kwargs)
            print(ItemData.objects.filter(item_id=kwargs['item_id']))
            return ItemData.objects.filter(item_id=kwargs['item_id'])
        elif 'item_id' in kwargs and 'market' in kwargs:
            return eyeballs[kwargs['market']].get_item(**kwargs)
        else:
            return get_object_or_404(ItemData.objects.filter(item_id=kwargs['item_id']))
