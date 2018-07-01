from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView
from .models import ItemData
from beholder.eyeballs import session
from beholder.eyeballs import Eyes


def itemsList(request):
    kwargs = request.GET.dict()

    if 'item_id' in kwargs:
        return redirect('inventory:ItemDetails')
    else:
        session.data['Inventory'] = {obj.item_id: obj.data for obj in ItemData.objects.all()[:19]}
        session.save()
        return render(request, 'inventory/home.html', context={'session': session.data})


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
            Eyes['ebay'].getItemPriceHistories(**kwargs)
            return ItemData.objects.get(item_id=kwargs['get_prices'])

        elif 'capture' in session.data.keys():
            return {**ItemData.objects.get(item_id=session.data['capture']['item_id']).data, **kwargs}
        else:
            return get_object_or_404(ItemData.objects.filter(item_id=kwargs['item_id']))
