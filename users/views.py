from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import (
    LoginView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView)

from .forms import (
    CustomUserCreationForm, 
    CustomLoginForm, 
    EmailValidationOnForgotPassword,
    PasswordConfirmationForm)

"""
    [Source]
    https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordChangeView
"""

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    

class LoginUserView(LoginView):
    template_name = 'registration/login.html'
    form_class  = CustomLoginForm
    

class ResetPassWord(PasswordResetView):
    template_name = 'registration/password_reset.html'
    form_class = EmailValidationOnForgotPassword
    success_url='registration/reset_password_reset_done.html'
    from_email = 'y.m.lima19@gmail.com'
    # extra_context = 'Dict'

class ResetPassWordDone(PasswordResetDoneView):
    template_name= 'registration/password_reset_done.html'
    # extra_context = 'Dict'

class ResetPassWordConfirmation(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = PasswordConfirmationForm
    success_url = 'registration/password_reset_complete.html'
    # extra_context = 'Dict'

class ResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    # extra_context = 'Dict'