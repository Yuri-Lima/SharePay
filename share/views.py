from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy 
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel, 
    SubHouseNameModel,
    SubTenantModel,
    SubKilowattModel)
from .forms import (
    HouseNameFormset,
    HouseBillFormset,
    HouseKilowattsFormset,
    SubHouseNameFormset,
    SubHouseKilowattFormset,
    )
from django.views.generic import (
    CreateView,
    TemplateView,
    DeleteView,
    FormView,
    ListView,
    DetailView,
    UpdateView,
    RedirectView)
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
    fields = ['house_name', 'meter', 'main_house']
    
    

    def form_valid(self, form):
        #Set User
        form.instance.user_FK =  self.request.user

        messages.add_message(
            self.request, 
            messages.INFO,
            'The House Name has been added'
        )
        return super(HouseNameCreateView, self).form_valid(form)

class PreHouseNameDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = HouseNameModel
    template_name = 'houses/pre/pre_detail_house_name.html'
    context_object_name = 'house'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # print(f'OBJECT:{self.object}') 
        object_list = SubTenantModel.objects.filter(main_tenant_FK=self.object)
        context = super(PreHouseNameDetailView, self).get_context_data(object_list= object_list, **kwargs)
        return context

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

class SubHouseNameDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = HouseNameModel
    template_name = 'houses/detail_sub_house_name.html'
    context_object_name = 'house'
    paginate_by = 2

    #Activate PAGINATIONS
    def get_context_data(self, **kwargs):
        # print(f'Objects: {self.object.id}')
        object_list = SubHouseNameModel.objects.filter(sub_house_FK=self.object.id)
        context = super(SubHouseNameDetailView, self).get_context_data(object_list= object_list, **kwargs)
        return context
      
class HouseNameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HouseNameModel
    template_name = 'houses/update_house_name.html'
    fields = ['house_name', 'meter', 'main_house']
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
            messages.add_message(
                self.request, 
                messages.INFO,
                "House Name has been Deleted."
            )  
            return True
        return False
    
class HouseNameFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add/add_tenant_name.html'
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
    template_name = 'houses/add/add_house_bill.html'
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

class SubHouseNameFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add/add_sub_house.html'
    context_object_name = 'sub_houses'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(SubHouseNameFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(SubHouseNameFormView, self).post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = SubHouseNameFormset(**self.get_form_kwargs(), instance=self.object)       
        return formset # inline FormSet

    def form_valid(self, form) :
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Sub House Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())

class HouseKilowattsFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseKilowattModel 
    template_name = 'houses/add/add_house_kwh.html'
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
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Kilowatts Details Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())
    
    # def reverse_url(self):
    #     return reverse('share:add_house_kwh', kwargs={'pk': self.object.pk})
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})


    
    # def reverse_url(self):
    #     return reverse('share:add_house_kwh', kwargs={'pk': self.object.pk})
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})

class SubHouseKilowattsFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel 
    template_name = 'houses/add/add_sub_house_kwh.html'
    context_object_name = 'houseskwh'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(SubHouseKilowattsFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(SubHouseKilowattsFormView, self).post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = SubHouseKilowattFormset(**self.get_form_kwargs(), instance=self.object)       
        return formset # inline FormSet

    def form_valid(self, form) :
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Sub Kilowatts Details Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())
    
    # def reverse_url(self):
    #     return reverse('share:add_house_kwh', kwargs={'pk': self.object.pk})
        
    def get_success_url(self):
        return reverse('share:pre_detail_house_name', kwargs={'pk': self.object.pk})