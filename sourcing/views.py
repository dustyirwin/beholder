from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404
from django.views.generic import DetailView, ListView


def query(request):
    return render(request, 'sourcing/query.html')


def response(request):
    return render(request, 'sourcing/response.html')
