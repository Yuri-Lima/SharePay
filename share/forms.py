from .models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel)
from django.forms.models import inlineformset_factory

HouseNameFormset = inlineformset_factory(
    HouseNameModel,
    HouseTenantModel,
    fields=['house_tenant', 'start_date', 'end_date'],
    extra=1,
    min_num=1,
    can_delete=True,
    can_order=True
)

HouseBillFormset = inlineformset_factory(

    HouseNameModel, 
    HouseBillModel,
    fields=['amount_bill', 'start_date_bill', 'end_date_bill'], 
    extra=0, 
    min_num=1,
    max_num=2,
    can_delete=True,
    can_order=True
)

HouseKilowattsFormset = inlineformset_factory(

    HouseNameModel, 
    HouseKilowattModel,
    fields=['kwh', 'last_read_kwh', 'read_kwh'], 
    extra=0, 
    min_num=1,
    max_num=2,
    can_delete=True,
    can_order=True
)
