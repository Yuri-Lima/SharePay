from django.contrib import admin
from .models import (
    HouseNameModel,
    HouseTenantModel,
    HouseBillModel,
    HouseKilowattModel,
    SubHouseNameModel,
    SubKilowattModel,
    SubTenantModel
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

@admin.register(SubHouseNameModel)
class SubHouseNameModelAdmin(admin.ModelAdmin):
    list_display = ['sub_house_FK','sub_house_name', 'sub_meter', 'sub_main_house', 'sub_last_updated_house']

@admin.register(SubKilowattModel)
class SubKilowattModelAdmin(admin.ModelAdmin):
    list_display = ['main_house_kwh_FK', 'sub_house_kwh_FK','sub_kwh', 'sub_last_read_kwh', 'sub_read_kwh', 'sub_last_updated_kwh']

@admin.register(SubTenantModel)
class SubTenantModelAdmin(admin.ModelAdmin):
    list_display = ['main_tenant_FK', 'sub_house_tenant_FK','sub_house_tenant', 'sub_start_date', 'sub_end_date', 'sub_days', 'sub_last_updated_tenant']
