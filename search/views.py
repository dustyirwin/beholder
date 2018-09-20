from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from inventory.models import ItemData
from .forms import QueryMarket
#from .models import Query, Resp
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
        kwargs['market_names'] = [k[:-5] for k in kwargs if '_page' in k]

        if 'keywords' in request.GET:
            self.eye.search(**kwargs)

        else:
            pass  # todo: user requests page change
        session = self.eye.open(request.user)
        session.data['kwargs'] = kwargs

        # construct page context from object_ids
        for market_name, market in session.data['market_datas'].items():

            if 'object_ids' in session.data['market_datas'][market_name]:
                object_ids = session.data['market_datas'][market_name]['object_ids']
                objects = [ItemData.objects.get(item_id=obj_id).data for obj_id in object_ids]
                objects = [{k: v[-1][0] if type(v) == list else v for k, v in obj.items()} for obj in objects]
                session.data['market_datas'][market_name]['objects'] = objects

            else:
                session.data['market_datas'][market_name]['objects'] = None

        return render(request, self.template_name, context={'session': session.data})

    def post(self, request):
        kwargs = request.POST.dict()
        return redirect('inventory:details', item_id=kwargs['capture'])
