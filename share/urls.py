from django.urls import path
from .views import IndexTemplateView

app_name = 'share'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('sharepay/', HousesNameListView.as_view(), name='houses_name_list'),
    path('sharepay/add/', HousesNameCreateView.as_view(), name='houses_name_create'),
    path('sharepay/<int:pk>/', HousesNameDetailView.as_view(), name='houses_name_detail'),
    path('sharepay/<int:pk>/tenant/edit/', HousesNameUpdateView.as_view(), name='houses_name_edit'),
    path('sharepay/<int:pk>/bill/edit/', HousesBillUpdateView.as_view(), name='houses_bill_add'),



    #Authenticaios Users
    # path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),#from django.contrib.auth import views as auth_views
    # path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]