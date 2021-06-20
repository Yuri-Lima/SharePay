from django.db.models.base import Model
from django import forms
from django.db.models.fields import CharField
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, TextInput, DateInput, fields, BaseModelFormSet, Field
from pytz import NonExistentTimeError
from share.models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel,
    SubHouseNameModel,
    SubTenantModel,
    SubKilowattModel,
)
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.http import request

""" CALENDAR """
class HouseNameDateInput(DateInput):
    input_type = 'date'
    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super(HouseNameDateInput, self).__init__(**kwargs) 

class HouseNameModelForm(forms.ModelForm):
    class Meta:
        model= HouseNameModel
        fields='__all__'  

class HouseTenantModelForm(forms.ModelForm):
    class Meta:
        model= HouseTenantModel
        fields='__all__'

    def clean(self):
        """
            A data inicial do Tenant nao deve ser menor que a data inicial da bill
            A data final do Tenant nao deve ser maior que a data final da bill
        """
        #First Validation
        #Data Range Validation
        obj_house_name=HouseNameModel.objects.get(pk=self.cleaned_data['house_name_FK'].id)
        start_date, end_date = False, False
        for obj_house_bill in obj_house_name.house_bill_related.all():
            if date.fromisoformat(str(self.cleaned_data['start_date'])) < date.fromisoformat(str(obj_house_bill.start_date_bill)):
                start_date = True
            if date.fromisoformat(str(self.cleaned_data['end_date'])) > date.fromisoformat(str(obj_house_bill.end_date_bill)):
                end_date = True

            if start_date and end_date:
                raise ValidationError({
                    'start_date': _(f'Out of Range - {obj_house_bill.start_date_bill}'),
                    'end_date': _(f'Out of Range - {obj_house_bill.end_date_bill}')
                })
            elif start_date:
                raise ValidationError({
                    'start_date': _(f'Out of Range - {obj_house_bill.start_date_bill}')
                })
            elif end_date:
                raise ValidationError({
                    'end_date': _(f'Out of Range - {obj_house_bill.end_date_bill}')
                })

        self.cleaned_data['days'] = int((self.cleaned_data['end_date'] - self.cleaned_data['start_date']).days)
        if self.cleaned_data['days'] < 0:
            raise ValidationError({
                'start_date': _('Start_Date has to be smaller than End_date'),
                'end_date': _('End_Date has to be bigger than Start_date')
            })
        return super(HouseTenantModelForm, self).clean()

class HouseBillModelForm(forms.ModelForm):
    class Meta:
        model= HouseBillModel
        fields=['house_bill_FK', 'amount_bill', 'start_date_bill', 'end_date_bill', 'days_bill']
    
    def clean(self):
        """
           'Val-1'--> Convert Masked Text to Decimal and check if it is a positive number.
                This check will be removed soon, it is just in case. Once we are using Mask Js.
           'Val-2'--> Set total bill's day and check if the start ou end dates are inverted. 
        """
        #Val -1
        self.cleaned_data['amount_bill'] = Decimal(self.cleaned_data['amount_bill'].replace(',',''))
        if self.cleaned_data['amount_bill'] < 0:
            raise ValidationError({
                'amount_bill': _('Should be a positive number!'),
            })
        #Val -2
        self.cleaned_data['days_bill'] = int((self.cleaned_data['end_date_bill'] - self.cleaned_data['start_date_bill']).days)
        if self.cleaned_data['days_bill'] < 0:
            raise ValidationError({
                'start_date_bill': _('Start_Date has to be smaller than End_date'),
                'end_date_bill': _('End_Date has to be bigger than Start_date')
            })

        return super(HouseBillModelForm, self).clean()

class HouseKilowattModelForm(forms.ModelForm):
    class Meta:
        model= HouseKilowattModel
        fields=['kwh', 'last_read_kwh', 'read_kwh']

class SubHouseNameModelForm(forms.ModelForm):
    class Meta:
        model= SubHouseNameModel
        fields= '__all__'

    
    #Overriding
    def clean(self):
        #Size Validation
        sub_house_name = self.cleaned_data['sub_house_name']
        lenght_name = len(sub_house_name) if sub_house_name else None
        if sub_house_name:
                if lenght_name > 25:
                    raise ValidationError({
                        'sub_house_name': _(f'Ensure House Name has max 25 characters (it has {lenght_name}).'),
                    })
        return super(SubHouseNameModelForm, self).clean()

class SubKilowattModelForm(forms.ModelForm):
    class Meta:
        model= SubKilowattModel
        fields=['sub_house_kwh_FK', 'sub_kwh', 'sub_amount_bill','sub_last_read_kwh', 'sub_read_kwh']

class SubTenantNameModelForm(forms.ModelForm):
    class Meta:
        model= SubTenantModel
        fields=['main_tenant_FK', 'sub_house_tenant_FK', 'sub_house_tenant', 'sub_start_date', 'sub_end_date', 'sub_days']
    
    def __init__(self, *args, **kwargs):
        self.pkform = kwargs.pop('pkform')
        super(SubTenantNameModelForm, self).__init__(*args, **kwargs)
        # self.fields['main_tenant_FK'].queryset = self.account
        
    def clean(self):
        #Muito Dificil
       #A data inicial do SubTenant nao deve ser menor que a data inicial da bill
       #A data final do SubTenant nao deve ser maior que a data final da bill

        obj_house_name=HouseNameModel.objects.get(pk=self.pkform)
        start_date, end_date = False, False
        for obj_house_bill in obj_house_name.house_bill_related.all():
            if date.fromisoformat(str(self.cleaned_data['sub_start_date'])) < date.fromisoformat(str(obj_house_bill.start_date_bill)):
                start_date = True
            if date.fromisoformat(str(self.cleaned_data['sub_end_date'])) > date.fromisoformat(str(obj_house_bill.end_date_bill)):
                end_date = True

            if start_date and end_date:
                raise ValidationError({
                    'sub_start_date': _(f'Out of Range- {obj_house_bill.start_date_bill}'),
                    'sub_end_date': _(f'Out of Range- {obj_house_bill.end_date_bill}')
                })
            elif start_date:
                raise ValidationError({
                    'sub_start_date': _(f'Out of Range- {obj_house_bill.start_date_bill}'),
                })
            elif end_date:
                raise ValidationError({
                    'sub_end_date': _(f'Out of Range- {obj_house_bill.end_date_bill}')
                })

        self.cleaned_data['sub_days'] = int((self.cleaned_data['sub_end_date'] - self.cleaned_data['sub_start_date']).days)
        if self.cleaned_data['sub_days'] < 0:
            raise ValidationError({
                'sub_start_date': _('Start_Date has to be smaller than End_date'),
                'sub_end_date': _('End_Date has to be bigger than Start_date')
            })

        # self.cleaned_data['sub_days'] = int((self.cleaned_data['sub_end_date'] - self.cleaned_data['sub_start_date']).days)
        return super(SubTenantNameModelForm, self).clean()

HouseNameFormset = inlineformset_factory(

    HouseNameModel,
    HouseTenantModel,
    form=HouseTenantModelForm,
    # formset=CustomFormSetBase_HouseNameFormset,
    # fields=['house_tenant', 'start_date', 'end_date'],
    extra=0,
    min_num=1,
    max_num=20,
    can_delete=True,
    can_order=True,
    error_messages={
        'unique': ('TESTE1'),
    },
    widgets={
        'house_tenant': TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Enter Tenant Name...',
            'aria-label': 'Enter Tenant Name...',
            'aria-describedby':'submit-button',
            'id': 'inputName',
            'type':'text',
        }),
        'start_date': HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'class': 'form-control',
                'id': 'inputStartDay',
                'type':'date',
                'required':'True',
            }),
        'end_date' : HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'class': 'form-control',
                'id': 'inputEndDay',
                'type':'date',
                'required':'True',
            }),
    },
)

HouseBillFormset = inlineformset_factory(

    HouseNameModel, 
    HouseBillModel,
    form=HouseBillModelForm,
    # fields=['house_bill_FK', 'amount_bill', 'start_date_bill', 'end_date_bill'], 
    extra=0, 
    min_num=1,
    max_num=2,
    can_delete=True,
    can_order=True,
    widgets={
        'amount_bill' : TextInput(attrs={'class': 'id_amount_bill'}),
        'start_date_bill': HouseNameDateInput(format=['%Y-%m-%d'],),
        'end_date_bill' : HouseNameDateInput(format=['%Y-%m-%d'],),
    },
)

HouseKilowattsFormset = inlineformset_factory(

    HouseNameModel, 
    HouseKilowattModel,
    form=HouseKilowattModelForm,
    # fields=['kwh', 'last_read_kwh', 'read_kwh'], 
    extra=0, 
    min_num=1,
    max_num=2,
    can_delete=True,
    can_order=True,
    widgets={
        'kwh': TextInput(attrs={
            'placeholder': 'Units Kilowatts...',  
        }),
        'last_read_kwh' : TextInput(attrs={
            'placeholder': 'Previous read...',
        }),
        'read_kwh' : TextInput(attrs={
            'placeholder': 'Present read...',
        }),
    },
)

SubHouseNameFormset = inlineformset_factory(

    HouseNameModel, 
    SubHouseNameModel,
    form=SubHouseNameModelForm,
    # fields=['sub_house_FK','sub_house_name', 'sub_meter', 'sub_main_house'], 
    extra=2, 
    min_num=1,
    max_num=3,
    can_delete=True,
    can_order=True,
    error_messages={
        'unique': ('TESTE2'),
    },
)

SubHouseKilowattFormset = inlineformset_factory(

    SubHouseNameModel,
    SubKilowattModel,
    form=SubKilowattModelForm,
    # fields=['main_house_kwh_FK','sub_house_kwh_FK', 'sub_kwh', 'sub_last_read_kwh', 'sub_read_kwh'],
    extra=0,
    min_num=1,
    max_num=2,
    can_delete=True,
    can_order=True,
)

SubHouseTenantFormset = inlineformset_factory(

    SubHouseNameModel,
    SubTenantModel,
    form=SubTenantNameModelForm,
    # fields=['main_tenant_FK', 'sub_house_tenant_FK', 'sub_house_tenant', 'sub_start_date', 'sub_end_date', 'sub_days'],
    extra=0,
    min_num=1,
    max_num=10,
    can_delete=True,
    can_order=True,
    widgets={
        'sub_house_tenant': TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Enter Sub Tenant Name...',
            'aria-label': 'Enter Sub Tenant Name...',
            'id': 'inputSubName',
            'type':'text',
        }),
        'sub_start_date': HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                    'class': 'form-control',
                    'id': 'inputSubStartDay',
                    'type':'date',
                    'required':'True',
                }),
        'sub_end_date' : HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'class': 'form-control',
                'id': 'inputSubEndDay',
                'type':'date',
                'required':'True',
            }), 
    },
)