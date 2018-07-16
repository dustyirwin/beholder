from django import forms
from django.contrib.auth.models import User


class SearchForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'session_data']
