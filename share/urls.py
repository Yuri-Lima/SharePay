from django.urls import path
from .views import (
    IndexTemplateView,
    
    HouseNameListView,

    HouseNameCreateView, 

    HouseNameDetailView,
    PreHouseNameDetailView,
    SubHouseNameListDetailView,
    SubHouseNameDetailView,

    HouseNameFormView,
    HouseBillFormView,
    HouseKilowattsFormView,
    SubHouseNameFormView,
    SubHouseKilowattsFormView,

    HouseNameUpdateView,
    HouseNameDeleteView,
)

app_name = 'share'

urlpatterns = [
    #Firts View
    path('', IndexTemplateView.as_view(), name='index'),
    
    #If there no House Name Registered
    path('create_house_name/add/', HouseNameCreateView.as_view(), name='create_house_name'),
    
    #Second View
    path('list_house_name/', HouseNameListView.as_view(), name='list_house_name'),
    
    #Options Views in list
    path('update_house_name/update/<int:pk>/', HouseNameUpdateView.as_view(), name='update_house_name'),
    path('delete_house_name/<int:pk>/delete', HouseNameDeleteView.as_view(), name='delete_house_name'),
    
    #Third View
    path('pre_detail_house_name/<int:pk>/', PreHouseNameDetailView.as_view(), name='pre_detail_house_name'),
    
    #Fourth View
    path('detail_house_name/<int:pk>/', HouseNameDetailView.as_view(), name='detail_house_name'),
    path('list_detail_sub_house_name/<int:pk>/', SubHouseNameListDetailView.as_view(), name='list_detail_sub_house_name'),
    path('detail_sub_house_name/<int:pk>/<int:subpk>/', SubHouseNameDetailView.as_view(), name='detail_sub_house_name'),

    #Fifth View
    path('add_house_bill/<int:pk>/bill/edit/', HouseBillFormView.as_view(), name='add_house_bill'),
    path('add_house_kwh/<int:pk>/kwh/edit/', HouseKilowattsFormView.as_view(), name='add_house_kwh'),
    path('add_tenant_name/<int:pk>/tenant/edit/', HouseNameFormView.as_view(), name='add_house_tenant_name'), 
    path('add_sub_house/<int:pk>/subhouse/edit/', SubHouseNameFormView.as_view(), name='add_sub_house'),
    path('add_sub_house_kwh/<int:pk>/subkwh/edit/<int:subpk>/', SubHouseKilowattsFormView.as_view(), name='add_sub_house_kwh'),
]