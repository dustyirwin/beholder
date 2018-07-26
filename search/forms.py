from django import forms
from django.contrib.postgres.fields import JSONField


class SearchForm(forms.Form):
    market_name=forms.CharField(max_length=32)
    categories=JSONField(default={})
    search_filters=JSONField(default={})
