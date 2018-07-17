from django import forms
from .models import SearchParams

class SearchForm(forms.ModelForm):

    class Meta:
        model = SearchParams
        fields = ['market_name', 'search_filters', 'categories']
