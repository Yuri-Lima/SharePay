from django.urls import path
from .views import (
    IndexTemplateView,
    HouseNameListView, 
    HouseNameCreateView, 
    HouseNameDetailView,
    HouseNameFormView,
    HouseBillFormView,
)

app_name = 'share'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('sharepay/', HouseNameListView.as_view(), name='list_house_name'),
    path('sharepay/add/', HouseNameCreateView.as_view(), name='create_house_name'),
    path('sharepay/<int:pk>/', HouseNameDetailView.as_view(), name='detail_house_name'),
    path('sharepay/<int:pk>/tenant/edit/', HouseNameFormView.as_view(), name='edit_house_name'),
    path('sharepay/<int:pk>/bill/edit/', HouseBillFormView.as_view(), name='add_house_bill'),



    #Authenticaios Users
    # path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),#from django.contrib.auth import views as auth_views
    # path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]