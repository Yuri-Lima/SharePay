from django.urls import path
from .views import (
    IndexTemplateView,
    
    HouseNameListView, 
    HouseNameCreateView, 
    HouseNameDetailView,

    HouseNameFormView,
    HouseBillFormView,
    HouseKilowattsFormView,

    HouseNameUpdateView,
    HouseNameDeleteView,
)

app_name = 'share'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('sharepay/', HouseNameListView.as_view(), name='list_house_name'),
    path('sharepay/add/', HouseNameCreateView.as_view(), name='create_house_name'),
    path('sharepay/<int:pk>/', HouseNameDetailView.as_view(), name='detail_house_name'),

    path('sharepay/<int:pk>/tenant/edit/', HouseNameFormView.as_view(), name='add_house_name'),
    path('sharepay/<int:pk>/bill/edit/', HouseBillFormView.as_view(), name='add_house_bill'),
    path('sharepay/<int:pk>/kwh/edit/', HouseKilowattsFormView.as_view(), name='add_house_kwh'), 

    path('sharepay/update/<int:pk>/', HouseNameUpdateView.as_view(), name='update_house_name'),
    path('sharepay/<int:pk>/delete', HouseNameDeleteView.as_view(), name='delete_house_name'),

]