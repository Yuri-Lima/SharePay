from django.forms.models import inlineformset_factory
from django.forms import ModelForm, TextInput, DateInput
from share.models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel,
)

class HouseNameDateInput(DateInput):
    input_type = 'date'
    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super(HouseNameDateInput, self).__init__(**kwargs) 
    

HouseNameFormset = inlineformset_factory(
    HouseNameModel,
    HouseTenantModel,
    fields=['house_tenant', 'start_date', 'end_date'],
    extra=1,
    min_num=1,
    can_delete=True,
    can_order=True,
    widgets={
        'start_date': HouseNameDateInput(format=['%Y-%m-%d'],),
        'end_date' : HouseNameDateInput(format=['%Y-%m-%d'],),
    },
)

HouseBillFormset = inlineformset_factory(

    HouseNameModel, 
    HouseBillModel,
    fields=['amount_bill', 'start_date_bill', 'end_date_bill'], 
    extra=0, 
    min_num=1,
    max_num=2,
    can_delete=True,
    can_order=True,
    widgets={
        'start_date_bill': HouseNameDateInput(format=['%Y-%m-%d'],),
        'end_date_bill' : HouseNameDateInput(format=['%Y-%m-%d'],),
    },

)

HouseKilowattsFormset = inlineformset_factory(

    HouseNameModel, 
    HouseKilowattModel,
    fields=['kwh', 'last_read_kwh', 'read_kwh'], 
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

