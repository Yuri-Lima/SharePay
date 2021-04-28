from django.contrib import admin
from .models import HouseNameModel,HouseTenantModel, HouseBillModel 


@admin.register(HouseNameModel)
class HouseNameAdmin(admin.ModelAdmin):
    list_display = ['house_name', 'meter'] 

@admin.register(HouseTenantModel)
class HouseTenantsAdmin(admin.ModelAdmin):
    list_display = ['house_name_FK', 'house_tenant']

@admin.register(HouseBillModel)
class HouseBillAdmin(admin.ModelAdmin):
     list_display = ['house_bill_FK','amount_bill','start_date_bill', 'end_date_bill','days_bill']