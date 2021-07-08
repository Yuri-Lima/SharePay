from share.models import HouseBillModel, HouseNameModel
from users.models import CustomUser
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import DeleteView, FormView
from django.shortcuts import render
from django.http.response import HttpResponseRedirect

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
    template_name= 'account/email.html'
    form_class = CustomAddEmailAccount

class ConnectionsUserView(ConnectionsView):
    # template_name = 'account/password_reset_confirm_new.html'
    form_class = DisconnectFormAccount
    # success_url = reverse_lazy('users:password_reset_complete')
    post_reset_login = True #A boolean indicating if the user should be automatically authenticated after a successful password reset
    # extra_context = 'Dict'

class ExcludeUserData(DeleteView):
    queryset = CustomUser.objects.all()
    template_name = 'account/delete_user_data.html'
    success_url = reverse_lazy('share:index')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

def privacy_policy(request):
    template_name = 'account/privacy_policy.html'
    content_type = 'text/html'
    return render(request, template_name)

def service_term(request):
    template_name = 'account/service_term.html'
    content_type = 'text/html'
    return render(request, template_name)


