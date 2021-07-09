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
    ExcludeUserData,

    ProfileUserView,

    privacy_policy,
    service_term
    )


app_name = 'users'

urlpatterns = [

    #Authenticaios Users
    path('accounts/signup/', SignUpUserView.as_view(), name='account_signup'),
    path('accounts/login/',  LoginUserView.as_view(), name='account_login'), 
    path('accounts/logout/', LogoutUserView.as_view(), name='account_logout'),

    #Profile Users
    path('welcome/profile/<int:pk>/', ProfileUserView.as_view(), name='profile'),

    #Password Reset
    path('accounts/password/set/', PasswordSetUserView.as_view(), name='account_set_password'),
    path('accounts/password/change/', PasswordChangeUserView.as_view(), name='account_change_password'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),

    #Email Management
    path('accounts/email/', EmailUserView.as_view(), name='account_email'),

    #Social Connections
    path('accounts/social/connections/', ConnectionsUserView.as_view(), name='socialaccount_connections'),  

    #Profiles
    path('exclude-all-user-data/<int:pk>/', ExcludeUserData.as_view(), name='delete_user_data'),

    #Privacy Policy
    path('privacy-policy/', privacy_policy, name='account_privacy_policy'),

    #Service Term
    path('service-term/', service_term, name='account_service_term'),

]