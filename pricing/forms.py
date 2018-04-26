from django import forms

class searchEbay(forms.Form):
    query = forms.CharField(max_length=100)