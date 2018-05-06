from django.shortcuts import render, get_object_or_404, get_list_or_404, Http404
from django.views.generic import DetailView, ListView
from pricing.models import *
import mws

def index(request):
    return render(request,'sourcing/index.html')
