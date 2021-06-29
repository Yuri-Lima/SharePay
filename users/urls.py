from django.urls import path, include
from .views import (
    SignUpView,
    LoginUserView,
    ResetPassWord,
    ResetPassWordDone,
    ResetPassWordConfirmation,
    ResetCompleteView)
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    #Authenticaios Users
    path('login/',  LoginUserView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #Password Reset
    path('password-reset/', ResetPassWord.as_view(), name='password_reset'),
    path('password-reset/done/', ResetPassWordDone.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', ResetPassWordConfirmation.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', ResetCompleteView.as_view(), name='password_reset_complete'),
]