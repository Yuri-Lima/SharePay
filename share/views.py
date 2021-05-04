from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse, reverse_lazy 
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel)
from .forms import (
    HouseNameFormset,
    HouseBillFormset,
    HouseKilowattsFormset)
from django.views.generic import (
    CreateView,
    TemplateView,
    DeleteView,
    FormView,
    ListView,
    DetailView,
    UpdateView)
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    

class HouseNameListView(LoginRequiredMixin, ListView):
    model = HouseNameModel
    template_name = 'houses/list_house_name.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'housesnames' : HouseNameModel.objects.all().filter(user_FK=self.request.user), 
        }
        return super(HouseNameListView, self).get_context_data(**ctx)


class HouseNameCreateView(LoginRequiredMixin, CreateView):
    model = HouseNameModel
    template_name = 'houses/create_house_name.html'
    fields = ['house_name', 'meter'] 

    def form_valid(self, form):
        #Set User
        form.instance.user_FK =  self.request.user

        messages.add_message(
            self.request, 
            messages.INFO,
            'The House Name has been added'
        )
        return super(HouseNameCreateView, self).form_valid(form)

class HouseNameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HouseNameModel
    template_name = 'houses/update_house_name.html'
    fields = ['house_name', 'meter']
    context_object_name = 'house'

    def test_func(self):
        user = self.get_object()
        if user.user_FK == self.request.user:
            return True
        return False

class HouseNameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = HouseNameModel
    template_name = 'houses/delete_house_name.html'
    success_url = reverse_lazy('share:list_house_name')
    context_object_name = 'house'

    def test_func(self):
        user = self.get_object()
        if user.user_FK == self.request.user:
            return True
        return False
    

class HouseNameDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = HouseNameModel
    template_name = 'houses/detail_house_name.html'
    context_object_name = 'house'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # print(f'OBJECT:{self.object}') 
        object_list = HouseTenantModel.objects.filter(house_name_FK=self.object)
        context = super(HouseNameDetailView, self).get_context_data(object_list= object_list, **kwargs)
        return context
    
    


class HouseNameFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add_tenant_name.html'
    context_object_name = 'houses'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(HouseNameFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(HouseNameFormView, self).post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = HouseNameFormset(**self.get_form_kwargs(), instance=self.object)
        return formset # inline FormSet

    def form_valid(self, form) :
        # print(form)
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Tenant's Detail Was Informed."
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
        return super(HouseBillFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(HouseBillFormView, self).post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = HouseBillFormset(**self.get_form_kwargs(), instance=self.object)        
        return formset # inline FormSet

    def form_valid(self, form) :
        # print(form)
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Bill's Detail Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})

class HouseKilowattsFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add_house_kwh.html'
    context_object_name = 'houseskwh'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(HouseKilowattsFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(HouseKilowattsFormView, self).post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = HouseKilowattsFormset(**self.get_form_kwargs(), instance=self.object)       
        return formset # inline FormSet

    def form_valid(self, form) :
        # print(form)
        # print(form.instance.last_read_kwh)
        obj = self.get_object()
        kwh_objs = HouseKilowattModel.objects.all().filter(house_kwh_FK=self.object)
        for kwh_obj in kwh_objs:
            print(kwh_obj.last_read_kwh)
            print(kwh_obj.read_kwh) 
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Kilowatts/Hour Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})