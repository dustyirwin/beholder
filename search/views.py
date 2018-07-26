from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from inventory.models import ItemData
from .forms import SearchForm
from .models import SearchParams
from beholder.eyeballs import Eye
import asyncio
# import traceback


class IndexView(TemplateView):
    template_name = 'search/query.html'
    eye = Eye()


    def get(self, request):
        session = self.eye.open(request.user)
        search_params = SearchForm()
        return render(request, 'search/query.html', {'session': session.data})

    def post(self, request):
        session = self.eye.open(request.user)
        kwargs = request.POST.dict()
        kwargs['user'] = str(request.user)

        # gather additional details, capture item to db, and redirect to inventory:ItemDetails
        if 'capture' in kwargs:
            return redirect('inventory:details', item_id=kwargs['capture'])

        # activate user-requested marketplaces and query
        kwargs['market_names'] = [k[:-2] for k in kwargs if 'SE' in k and bool(k)]
        self.eye.search(**kwargs)

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
