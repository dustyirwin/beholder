from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from inventory.models import ItemData
from .forms import SearchForm
from .models import SearchParams
from beholder.eyeballs import Eye
import asyncio
# import traceback


class IndexView(TemplateView):
    template_name = 'search/response.html'
    eye = Eye()

    def get(self, request):
        kwargs = request.GET.dict()
        kwargs['user'] = request.user
        # activate user-requested marketplaces and query
        kwargs['markets'] = [k[:-5] for k in kwargs if '_page' in k and bool(k)]
        self.eye.search(**kwargs)
        session = self.eye.open(request.user)
        session.data['kwargs'] = kwargs

        # construct context from object_ids
        for market_name, market in session.data['market_data'].items():

            if 'object_ids' in session.data['market_data'][market_name]:
                object_ids = session.data['market_data'][market_name]['object_ids']
                objects = [ItemData.objects.get(item_id=item_id).data for item_id in object_ids]
                session.data['market_data'][market_name]['objects'] = objects

            else:
                session.data['market_data'][market_name]['objects'] = None

        return render(request, self.template_name, context={'session': session.data})

    def post(self, request):
        kwargs = request.POST.dict()
        return redirect('inventory:details', item_id=kwargs['capture'])
