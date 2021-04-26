from django.shortcuts import render
from django.views.generic import (CreateView, TemplateView, DeleteView, FormView, ListView)

# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'houses/index.html'

