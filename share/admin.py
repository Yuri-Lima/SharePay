from django.contrib import admin
from .models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel
    ) 


@admin.register(HouseNameModel)
class HouseNameAdmin(admin.ModelAdmin):
    list_display = ['house_name', 'meter', 'last_updated_house'] 

@admin.register(HouseTenantModel)
class HouseTenantsAdmin(admin.ModelAdmin):
    list_display = ['house_name_FK', 'house_tenant', 'last_updated_tenant']

@admin.register(HouseBillModel)
class HouseBillAdmin(admin.ModelAdmin):
     list_display = ['house_bill_FK','amount_bill','start_date_bill', 'end_date_bill','days_bill', 'last_updated_bill']

@admin.register(HouseKilowattModel)
class HouseKilowattAdmin(admin.ModelAdmin):
    list_display = ['house_kwh_FK','kwh', 'last_updated_kwh']
