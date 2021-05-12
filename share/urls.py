from django.urls import path
from .views import (
    IndexTemplateView,
    
    HouseNameListView,

    HouseNameCreateView, 

    HouseNameDetailView,
    PreHouseNameDetailView,
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
    path('create-sharepay/add/', HouseNameCreateView.as_view(), name='create_house_name'),
    
    #Second View
    path('list-sharepay/', HouseNameListView.as_view(), name='list_house_name'),
    
    #Options Views in list
    path('sharepay/update/<int:pk>/', HouseNameUpdateView.as_view(), name='update_house_name'),
    path('sharepay/<int:pk>/delete', HouseNameDeleteView.as_view(), name='delete_house_name'),
    
    #Third View
    path('pre-detail-sharepay/<int:pk>/', PreHouseNameDetailView.as_view(), name='pre_detail_house_name'),
    
    #Fourth View
    path('detail-sharepay/<int:pk>/', HouseNameDetailView.as_view(), name='detail_house_name'),
    path('detail-sub-sharepay/<int:pk>/', SubHouseNameDetailView.as_view(), name='sub_detail_house_name'),
    
    #Fifth View
    path('sharepay/<int:pk>/bill/edit/', HouseBillFormView.as_view(), name='add_house_bill'),
    path('sharepay/<int:pk>/kwh/edit/', HouseKilowattsFormView.as_view(), name='add_house_kwh'),
    path('sharepay/<int:pk>/tenant/edit/', HouseNameFormView.as_view(), name='add_house_tenant_name'), 
    path('sharepay/<int:pk>/subhouse/edit/', SubHouseNameFormView.as_view(), name='add_sub_house'),
    path('sharepay/<int:pk>/subkwh/edit/', SubHouseKilowattsFormView.as_view(), name='add_sub_house_kwh'),
]