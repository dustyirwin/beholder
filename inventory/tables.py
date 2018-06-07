import django_tables2 as tables
from django_tables2.utils import A
from .models import ItemData


class ItemTable(tables.Table):
    item_id = tables.LinkColumn('item-detail', args=[A('pk')])
    name = tables.LinkColumn('item-detail', args=[A('pk')])
    key1 = tables.LinkColumn('item-detail', args=[A('pk')])

    class Meta:
        model = ItemData
        fields = ('item_id', 'name', 'key1', )
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "Nothing here my friend..."
