from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import HouseNameModel, HouseTenantModel, HouseBillModel
from .forms import HouseNameFormset, HouseBillFormset 
from django.views.generic import (CreateView, TemplateView, DeleteView, FormView, ListView, DetailView)
from django.contrib.auth.models import User

# Create your views here.
"""Get any context"""
class IndexTemplateView(TemplateView):
    template_name = 'houses/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.id: 
            ctx = super().get_context_data(**kwargs)
            ctx = {
                'user' : self.request.user,
                'houses' : HouseNameModel.objects.all().filter(user_FK=self.request.user),
            }
            return ctx
    

class HouseNameListView(ListView):
    model = HouseNameModel
    template_name = 'houses/list_house_name.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'housesnames' : HouseNameModel.objects.all().filter(user_FK=self.request.user), 
        }
        return super().get_context_data(**ctx)


class HouseNameCreateView(LoginRequiredMixin, CreateView):
    model = HouseNameModel
    template_name = 'houses/create_house_name.html'
    fields = ['house_name', 'meter'] 

    def form_valid(self, form):
        #Set User
        form.instance.user_FK =  self.request.user

        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'The House Name has been added'
        )
        return super(HouseNameCreateView, self).form_valid(form)

    

class HouseNameDetailView(LoginRequiredMixin, DetailView):
    model = HouseNameModel
    template_name = 'houses/detail_house_name.html'
    context_object_name = 'house'


class HouseNameFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add_tenant_name.html'
    context_object_name = 'houses'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all().order_by('-id'))
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all().order_by('-id'))
        return super().post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = HouseNameFormset(**self.get_form_kwargs(), instance=self.object)
        return formset # inline FormSet

    def form_valid(self, form) :
        # print(form)
        form.save()
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'New House Name Was Added'
        )
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})

class HouseBillFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add_house_bill.html'
    context_object_name = 'housesbill'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super().post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = HouseBillFormset(**self.get_form_kwargs(), instance=self.object)
        return formset # inline FormSet

    def form_valid(self, form) :
        # print(form)
        form.save()
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'Bill Was Added'
        )
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})