from django.views.generic import ListView, DetailView
# from django.shortcuts import render
from beholder.eyeballs import eyeballs
from .models import ItemData


class ItemList(ListView):
    template_name = "inventory/home.html"
    context_object_name = 'items'
    ordering = ['id']

    def get_object(self):
        kwargs = self.request.GET.dict()
        return ItemData.objects.filter(**kwargs).order_by(kwargs['order_by'])


class ItemDetails(DetailView):
    template_name = "inventory/details.html"
    context_object_name = 'item'

    def get_object(self):
        kwargs = self.request.GET.dict()
        return eyeballs[kwargs['market']].get_item(**kwargs)
