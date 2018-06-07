from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import ItemData
from .tables import ItemTable
# Create your views here.

class ItemListView(ListView):
    items = ItemData
    template_name = "inventory/home.html"
    context_object_name = 'items'
    ordering = ['id']

    def get_query_set(self, **kwargs):
        context = super(ItemListView, self).get_query_set(**kwargs)
        table = ItemTable(items.objects.all())
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['table'] = table
        return context

class ItemDetailsView(DetailView):
    items = ItemData
    template_name = "inventory/details.html"
    context_object_name = 'item'

    def get_queryset(self, **kwargs):
        context = super(ItemDetailsView, self).get_queryset(**kwargs)
        item = items.objects.filter(data__key1="abcd")
        context['item'] = item
        return context
