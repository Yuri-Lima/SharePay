from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy 
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
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
    SubHouseTenantFormset,

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
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
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
    fields = ['house_name', 'meter',]

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

class SubHouseNameListDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = HouseNameModel
    template_name = 'houses/list_detail_sub_house_name.html'
    context_object_name = 'house'
    paginate_by = 2

    #Activate PAGINATIONS [MultipleObjectMixin]
    def get_context_data(self, **kwargs):
        # print(f'Objects: {self.object.id}')
        context = {
            'object_list': SubHouseNameModel.objects.filter(sub_house_FK=self.object.id),
        }
        return super(SubHouseNameListDetailView, self).get_context_data(**context)

class SubHouseNameDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model= HouseNameModel
    template_name= 'houses/detail_sub_house_name.html'
    context_object_name= 'house'
    paginate_by= 2

    #Activate PAGINATIONS [MultipleObjectMixin]
    def get_context_data(self, **kwargs):
        # print(f'kwargs: {self.kwargs["subpk"]}') 
        context = {
            'object_list': SubTenantModel.objects.filter(main_tenant_FK=self.object.id),
            'subhouse': SubHouseNameModel.objects.get(pk=self.kwargs['subpk'])
        }
        return super(SubHouseNameDetailView, self).get_context_data(**context)
      
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
        print(f'SubHouseNameFormView:\n {formset}')
        print(f'*'*10)      
        return formset # inline FormSet

    def form_valid(self, form) :
        # print(form)
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Sub House Name Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())#

    def get_success_url(self):
        return reverse('share:list_detail_sub_house_name', kwargs={'pk': self.kwargs['pk']})
    
class TenantsHouseNameFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = HouseNameModel
    template_name = 'houses/add/add_tenant_name.html'
    context_object_name = 'houses'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(TenantsHouseNameFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=HouseNameModel.objects.all())
        return super(TenantsHouseNameFormView, self).post(request, *args, **kwargs)

    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = HouseNameFormset(**self.get_form_kwargs(), instance=self.object)
        # print(f'TenantsHouseName:\n {formset}')
        # print(f'*'*10)
        return formset # inline FormSet

    def form_valid(self, form) :
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
        # print(form.has_changed())
        # if form.has_changed():
        #     form.update()
        # else:
        #     form.save()
        form.save()
        messages.add_message(
            self.request, 
            messages.INFO,
            "Bill's Detail Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        print('Invalid Form')
        return super().form_invalid(form)

class SubTenantsHouseNameFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = SubHouseNameModel
    template_name = 'houses/add/add_sub_house_tenant.html'
    context_object_name = 'sub_tenants'
    
    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = SubHouseNameModel.objects.get(pk=self.kwargs.get('subpk'))
        # print(self.object)
        return super(SubTenantsHouseNameFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = SubHouseNameModel.objects.get(pk=self.kwargs.get('subpk'))
        # print(self.object)
        return super(SubTenantsHouseNameFormView, self).post(request, *args, **kwargs)


    """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = SubHouseTenantFormset(**self.get_form_kwargs(), instance=self.object)
        print(f' SubTenantsHouse:\n {formset}')
        print(f'*'*10) 
        return formset # inline FormSet
    

    def form_valid(self, form) :
        form.save()
        #I had to do this, because up to now, it was what a learned.
        objs = SubTenantModel.objects.all().filter(sub_house_tenant_FK= self.object)
        for obj in objs:
            if not obj.main_tenant_FK:
                obj.main_tenant_FK = HouseNameModel.objects.get(pk=self.kwargs['pk']) 
                obj.save()
            if obj.sub_house_tenant == None:
                obj.delete()
        #END

        messages.add_message(
            self.request, 
            messages.INFO,
            "Sub Tenant Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('share:detail_sub_house_name', kwargs={
                                                            'pk': self.kwargs['pk'],
                                                            'subpk' : self.kwargs['subpk']
                                                            })

    def form_invalid(self, form):
        print('Invalid Form')
        return super().form_invalid(form)

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
        
    def get_success_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.object.pk})

class SubHouseKilowattsFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = SubHouseNameModel    
    template_name = 'houses/add/add_sub_house_kwh.html'
    context_object_name = 'houseskwh'

    """Handle GET requests: instantiate a blank version of the form."""
    def get(self, request, *args, **kwargs):
        self.object = SubHouseNameModel.objects.get(pk=self.kwargs.get('subpk'))
        return super(SubHouseKilowattsFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # self.object = self.get_object(queryset=HouseNameModel.objects.all())
        self.object = SubHouseNameModel.objects.get(pk=self.kwargs.get('subpk'))
        # print(self.object)
        return super(SubHouseKilowattsFormView, self).post(request, *args, **kwargs)

    # """Handle a Formset setting - Instansce get self.object which was set for HousesName by each user"""
    def get_form(self, form_class=None):
        formset = SubHouseKilowattFormset(**self.get_form_kwargs(), instance=self.object)
        # print(f' SubHouseKilowattsFormView:\n {formset}')
        # print(f'*'*10) 
        return formset # inline FormSet

    def form_valid(self, form): 
        form.save()
        objs = SubKilowattModel.objects.all().filter(sub_house_kwh_FK= self.object)
        for obj in objs:
            if not obj.main_house_kwh_FK:
                obj.main_house_kwh_FK = HouseNameModel.objects.get(pk=self.kwargs['pk']) 
                obj.save()
            
        messages.add_message(
            self.request, 
            messages.INFO,
            "Sub Kilowatts Details Was Informed."
        )
        return HttpResponseRedirect(self.get_success_url())
    
    # def form_invalid(self, form):
    #     print('Invalid Form')
    #     return super().form_invalid(form)
        
    def get_success_url(self):
        return reverse('share:detail_sub_house_name', kwargs={
                                                            'pk': self.kwargs['pk'],
                                                            'subpk' : self.kwargs['subpk']
                                                            })