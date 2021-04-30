from .models import HouseNameModel, HouseTenantModel, HouseBillModel
from django.forms.models import inlineformset_factory

HouseNameFormset = inlineformset_factory(HouseNameModel, HouseTenantModel ,fields=['house_tenant', 'start_date', 'end_date'], extra=1, can_delete=True, can_order=True)
HouseBillFormset = inlineformset_factory(HouseNameModel, HouseBillModel, fields=['amount_bill', 'start_date_bill', 'end_date_bill'], extra=0, max_num=2,  can_delete=True, can_order=True)
