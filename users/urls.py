from django.urls import path, include
from .views import (
    SignUpUserView,
    LoginUserView,
    LogoutUserView,
    PasswordSetUserView,
    PasswordChangeUserView,
    PasswordResetView,
    ConnectionsUserView,
    EmailUserView,
    )


app_name = 'users'

urlpatterns = [

    path('accounts/signup/', SignUpUserView.as_view(), name='account_signup'),
    #Authenticaios Users
    path('accounts/login/',  LoginUserView.as_view(), name='account_login'), 
    path('accounts/logout/', LogoutUserView.as_view(), name='account_logout'),

    #Password Reset
    path('accounts/password/set/', PasswordSetUserView.as_view(), name='account_set_password'),
    path('accounts/password/change/', PasswordChangeUserView.as_view(), name='account_change_password'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),

    #Email Management
    path('accounts/email/', EmailUserView.as_view(), name='account_email'),

    #Social Connections
    path('accounts/social/connections/', ConnectionsUserView.as_view(), name='socialaccount_connections'),  

    #Profiles
    # path('update/<int:pk>/', UpdateAccountView.as_view(), name='update'),

]