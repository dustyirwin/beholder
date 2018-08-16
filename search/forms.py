from django.forms import ModelForm
from search.models import Query
from django.contrib.postgres.fields import JSONField


class QueryMarket(ModelForm):
    class Meta:
        model = Query
        fields = ['active', 'market_name', 'category', 'filters']
