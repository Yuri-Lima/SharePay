from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import FormView

from allauth.account.views import(
    LoginView,
    SignupView,
    LogoutView,
    PasswordSetView,
    PasswordChangeView,
    PasswordResetView,
    EmailView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
    ConfirmEmailView,
)
from allauth.socialaccount.views import(
    ConnectionsView,
)

from .forms import (
    CustomLoginAccount,
    CustomSignupAccount,
    SetPasswordFormAccount,
    ChangePasswordFormAccount,
    ResetPasswordFormAccount,
    CustomAddEmailAccount,
    SignupFormSocialAccount,
    DisconnectFormAccount,
    )
from users.models import CustomUser

"""
    [Source]
    https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordChangeView
"""
class LoginUserView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('share:index')
    # form_class  = CustomLoginAccount

class SignUpUserView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomSignupAccount

class LogoutUserView(LogoutView):
    pass
    # template_name = 'account/signup.html'
    # form_class = CustomLoginAccount
    # success_url = reverse_lazy('users:account_login')

class PasswordSetUserView(PasswordSetView):
    form_class = SetPasswordFormAccount

class PasswordChangeUserView(PasswordChangeView):
    form_class = ChangePasswordFormAccount
    
class PasswordResetUserView(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = ResetPasswordFormAccount
    # success_url= reverse_lazy('users:password_reset_done')
    # email_template_name = 'account/resets_template/password_reset_email.html'
    # extra_context = 'Dict'

class PasswordResetFromKeyUserView(PasswordResetFromKeyView):
    template_name = 'account/password_reset.html'
    form_class = ResetPasswordFormAccount  

class PasswordResetFromKeyDoneUserView(PasswordResetFromKeyDoneView):
    template_name = 'account/password_reset_from_key_done.html'

class EmailUserView(EmailView):
    # template_name= 'account/password_reset_done.html'
    form_class = CustomAddEmailAccount
    # extra_context = 'Dict'

class ConnectionsUserView(ConnectionsView):
    # template_name = 'account/password_reset_confirm_new.html'
    form_class = DisconnectFormAccount
    # success_url = reverse_lazy('users:password_reset_complete')
    post_reset_login = True #A boolean indicating if the user should be automatically authenticated after a successful password reset
    # extra_context = 'Dict'
