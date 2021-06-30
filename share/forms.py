from django.db.models.base import Model
from django import forms
from django.db.models.fields import CharField
from django.forms.models import inlineformset_factory
from django.forms import TextInput, DateInput, NumberInput
from share.models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel,
    SubHouseNameModel,
    SubTenantModel,
    SubKilowattModel,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

""" CALENDAR """
class HouseNameDateInput(DateInput):
    input_type = 'date'
    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super(HouseNameDateInput, self).__init__(**kwargs) 

class HouseNameModelForm(forms.ModelForm):
    house_name = forms.TextInput(
        attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Enter House Name...',
            'aria-label': 'Enter House Name...',
            'aria-describedby':'submit-housename',
            'id': 'inputName',
            'type':'text',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add House Name",
            'required':'True',
        })
    class Meta:
        model= HouseNameModel
        fields=['house_name']

    def clean(self):
        house_name = self.cleaned_data['house_name']
        if house_name:
            if len(house_name) > 25:
                raise ValidationError({
                    'house_name': _(f'Ensure House Name has max 25 characters (it has {len(self.cleaned_data["house_name"])}).'),
                })
        else:
            raise ValidationError({
                'house_name': _('You must provide a House Name (up to 25 letters).'),
            })

        return super(HouseNameModelForm, self).clean()

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
        flag_start_date, flag_end_date = False, False
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        for obj_house_bill in obj_house_name.house_bill_related.all():
            if start_date < obj_house_bill.start_date_bill:
                flag_start_date = True
            if end_date > obj_house_bill.end_date_bill:
                flag_end_date = True

            if flag_start_date and flag_end_date:
                raise ValidationError({
                    'start_date': _(f'Out of Range - {obj_house_bill.start_date_bill}'),
                    'end_date': _(f'Out of Range - {obj_house_bill.end_date_bill}')
                })
            elif flag_start_date:
                raise ValidationError({
                    'start_date': _(f'Out of Range - {obj_house_bill.start_date_bill}')
                })
            elif flag_end_date:
                raise ValidationError({
                    'end_date': _(f'Out of Range - {obj_house_bill.end_date_bill}')
                })

        days = int((end_date - start_date).days)
        if days < 0:
            raise ValidationError({
                'start_date': _('Start_Date has to be smaller than End_date'),
                'end_date': _('End_Date has to be bigger than Start_date')
            })
        self.cleaned_data['days'] = days
        return super(HouseTenantModelForm, self).clean()

class HouseBillModelForm(forms.ModelForm):
    days_bill = forms.IntegerField(required=False)
    
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
        self.cleaned_data['amount_bill'] = float(self.cleaned_data['amount_bill'].replace(',',''))
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

    def clean(self):
        last_read_kwh = self.cleaned_data['last_read_kwh']
        read_kwh = self.cleaned_data['read_kwh']
        if last_read_kwh and read_kwh:
            if (last_read_kwh > read_kwh):
                raise ValidationError({
                    'read_kwh': _('Should be greatter than previous Kw/h read')
                })
            else:
                self.cleaned_data['kwh'] = read_kwh - last_read_kwh
        elif self.cleaned_data['kwh']:
            if self.cleaned_data['kwh'] < 0:
                raise ValidationError({
                    'kwh': _('Only Positive Number!')
                })
            elif self.cleaned_data['kwh'] >= 0:
                return super(HouseKilowattModelForm, self).clean()
        else:
            raise ValidationError({
                'kwh': _('Fill up at least one option!'),
                'last_read_kwh': _('Fill up at least one option!'),
                })
        return super(HouseKilowattModelForm, self).clean()

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
        fields=['main_house_kwh_FK', 'sub_house_kwh_FK', 'sub_kwh', 'sub_amount_bill','sub_last_read_kwh', 'sub_read_kwh']

    def __init__(self, *args, **kwargs):
        self.pkform = kwargs.pop('pkform')
        super(SubKilowattModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        all_obj = HouseNameModel.objects.get(pk=self.pkform)
        all_sub_kwh = all_obj.main_house_kilowatt_related.all()
        main = all_obj.house_kilowatt_related.all().first()
        sum_sub_kilowatts = int()
        for each in all_sub_kwh:
            sum_sub_kilowatts = sum_sub_kilowatts + each.sub_kwh
        
        if self.cleaned_data['sub_last_read_kwh'] and self.cleaned_data['sub_read_kwh']:
            if (self.cleaned_data['sub_last_read_kwh'] > self.cleaned_data['sub_read_kwh']):
                raise ValidationError({
                    'sub_read_kwh': _('Should be greatter than previous Kw/h read')
                    })
            else:
                self.cleaned_data['sub_kwh'] = self.cleaned_data['sub_read_kwh'] - self.cleaned_data['sub_last_read_kwh']
                sum_sub_kilowatts = sum_sub_kilowatts + self.cleaned_data['sub_kwh']
                if sum_sub_kilowatts > main.kwh:
                    raise ValidationError({
                            'sub_read_kwh': _(f'The total of the Sum is {sum_sub_kilowatts} kwh, it cannot be greatter than kilowatts from the bill. Registreded: Max{main.kwh} kwh')
                            })
        elif self.cleaned_data['sub_kwh']:
            if self.cleaned_data['sub_kwh'] < 0:
                raise ValidationError({
                        'sub_kwh': _('Only Positive Number!')
                        })
            elif self.cleaned_data['sub_kwh'] >= 0:
                sum_sub_kilowatts = sum_sub_kilowatts + self.cleaned_data['sub_kwh']
                if sum_sub_kilowatts > main.kwh:
                    raise ValidationError({
                            'sub_kwh': _(f'The total of the Sum is {sum_sub_kilowatts} kwh, it cannot be greatter than kilowatts from the bill. Registreded: Max{main.kwh} kwh')
                            })
                return super(SubKilowattModelForm, self).clean()
        elif (self.cleaned_data['sub_kwh'] and self.cleaned_data['sub_last_read_kwh'] and self.cleaned_data['sub_read_kwh']):
            raise ValidationError({
                'sub_kwh': _('Fill up at least one option!'),
                'sub_last_read_kwh': _('Fill up at least one option!'),

                })
        return super(SubKilowattModelForm, self).clean()

class SubTenantNameModelForm(forms.ModelForm):
    class Meta:
        model= SubTenantModel
        fields=['main_tenant_FK', 'sub_house_tenant_FK', 'sub_house_tenant', 'sub_start_date', 'sub_end_date', 'sub_days']
    
    def __init__(self, *args, **kwargs):
        self.pkform = kwargs.pop('pkform')
        super(SubTenantNameModelForm, self).__init__(*args, **kwargs)
        
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

HouseTenantFormset = inlineformset_factory(

    HouseNameModel,
    HouseTenantModel,
    form=HouseTenantModelForm,
    # formset=CustomFormSetBase_HouseTenantFormset,
    # fields=['house_tenant', 'start_date', 'end_date'],
    extra=0,
    min_num=1,
    max_num=20,
    can_delete=True,
    can_order=True,
    widgets={
        'house_tenant': TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Enter Tenant Name...',
            'aria-label': 'Enter Tenant Name...',
            'id': 'inputName',
            'type':'text',
            'required':'True',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add Tenant Name"
        }),
        'start_date': HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'class': 'form-control',
                'id': 'inputStartDay',
                'type':'date',
                'required':'True',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Srtat Date",
            }),
        'end_date' : HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'class': 'form-control',
                'id': 'inputEndDay',
                'type':'date',
                'required':'True',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add End Date",
            }),
    },
)

HouseBillFormset = inlineformset_factory(

    HouseNameModel, 
    HouseBillModel,
    form=HouseBillModelForm,
    # fields=['house_bill_FK', 'amount_bill', 'start_date_bill', 'end_date_bill', 'days_bill], 
    extra=0, 
    min_num=1,
    max_num=1,
    can_delete=True,
    can_order=True,
    widgets={
        'amount_bill' : NumberInput(
            attrs={
                'class': 'id_amount_bill',
                'id': 'inputAmountBill',
                'placeholder': 'Enter Amount...',
                'aria-label': 'Enter Amount...',
                'type':'text',
                'step':'0.01',
                'min' : '5.00',
                'max' : '500000.00', 
                'inputmode' : "decimal",
                'required':'True',
                'oninput':'validity.valid||(value="")',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Amount of the Bill",
                }),
        'start_date_bill': HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'id': 'inputStartDayBill',
                'type':'date',
                'required':'True',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Start Date",
            }),
        'end_date_bill' : HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'id': 'inputEndDayBill',
                'type':'date',
                'required':'True',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add End Date",
            }),
        'days_bill' : NumberInput(
            attrs={
                'id': 'inpuDaysBill',
                'type':'number',
                'required':'False',
            }),
    },
)

HouseKilowattsFormset = inlineformset_factory(

    HouseNameModel, 
    HouseKilowattModel,
    form=HouseKilowattModelForm,
    # fields=['kwh', 'last_read_kwh', 'read_kwh'], 
    extra=0, 
    min_num=1,
    max_num=1,
    can_delete=True,
    can_order=True,
    widgets={
        'kwh': NumberInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Units Kilowatts...',
                'aria-label': 'Units Kilowatts...',
                'id': 'inputKwh',
                'type':'number',
                'min':"0",
                'oninput':'validity.valid||(value="")',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Killowatts",
            }),
        'last_read_kwh' : NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Previous read...',
                'aria-label': 'Previous read...',
                'id': 'inputPreviousKwh',
                'type':'number',
                'min':"0",
                'oninput':'validity.valid||(value="")',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Last Read",
            }),
        'read_kwh' : NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Present read...',
                'aria-label': 'Present read...',
                'id': 'inputPresentKwh',
                'type':'number',
                'min':"0",
                'oninput':'validity.valid||(value="")',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Present Read",
            }),
    },
)

SubHouseNameFormset = inlineformset_factory(

    HouseNameModel, 
    SubHouseNameModel,
    form=SubHouseNameModelForm,
    # fields=['sub_house_FK','sub_house_name', 'sub_meter', 'sub_main_house'], 
    extra=1,
    min_num=1,
    max_num=5,
    can_delete=True,
    can_order=True,
    widgets={
        'sub_house_name': TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Enter Sub House Name...',
            'aria-label': 'Enter Sub House Name...',
            'id': 'inputSubHouseName',
            'type':'text',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add Sub House Name",
        }),
    }
)

SubHouseKilowattFormset = inlineformset_factory(

    SubHouseNameModel,
    SubKilowattModel,
    form=SubKilowattModelForm,
    # fields=['main_house_kwh_FK','sub_house_kwh_FK', 'sub_kwh', 'sub_last_read_kwh', 'sub_read_kwh'],
    extra=0,
    min_num=1,
    max_num=1,
    can_delete=True,
    can_order=True,
    widgets={
        'sub_kwh': NumberInput(attrs={
            'autofocus': True,
            'placeholder': 'Units Kilowatts...',
            'aria-label': 'Units Kilowatts...',
            'id': 'inputSubKwh',
            'type':'number',
            'min':"0",
            'oninput':'validity.valid||(value="")',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add Kilowatts",
        }),
        'sub_last_read_kwh' : NumberInput(attrs={
            'placeholder': 'Previous read...',
            'aria-label': 'Previous read...',
            'id': 'inputSubPreviousKwh',
            'type':'number',
            'min':"0",
            'oninput':'validity.valid||(value="")',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add Last Read",
        }),
        'sub_read_kwh' : NumberInput(attrs={
            'placeholder': 'Present read...',
            'aria-label': 'Present read...',
            'id': 'inputSubPresentKwh',
            'type':'number',
            'min':"0",
            'oninput':'validity.valid||(value="")',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add Present Read",
        }),
    },
)

SubHouseTenantFormset = inlineformset_factory(

    SubHouseNameModel,
    SubTenantModel,
    form=SubTenantNameModelForm,
    # fields=['main_tenant_FK', 'sub_house_tenant_FK', 'sub_house_tenant', 'sub_start_date', 'sub_end_date', 'sub_days'],
    extra=0,
    min_num=1,
    max_num=20,
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
            'required':'True',
            'data-toggle': "tooltip",
            'data-placement': "top",
            'title': "Add Tenant Name"
        }),
        'sub_start_date': HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputSubStartDay',
                'type':'date',
                'required':'True',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add Start Date"
            }),
        'sub_end_date' : HouseNameDateInput(format=['%Y-%m-%d'],
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'id': 'inputSubEndDay',
                'type':'date',
                'required':'True',
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': "Add End Date"
            }), 
    },
)