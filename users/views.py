from django.contrib.auth.models import UserManager
from users.models import CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.shortcuts import render
from django.http.response import HttpResponseRedirect

from allauth.account import signals

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
    CustomUserChangeForm
    )
from django.contrib.auth.models import AnonymousUser


"""
    [Source]
    https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordChangeView
"""
class ProfileUserView(UpdateView):
    model = CustomUser
    template_name = 'account/profile.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('share:index')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=CustomUser.objects.all())
        return super(ProfileUserView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        super(ProfileUserView, self).post(request, *args, **kwargs)
        self.object = self.get_object(queryset=CustomUser.objects.all())
        
        form = self.get_form()
        if form.is_valid():
            print(form)
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)
        # return super(ProfileUserView, self).post(request, *args, **kwargs)


class LoginUserView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('share:index')
    # form_class  = CustomLoginAccount
    def get_context_data(self, **kwargs):
        ctx = {
            'AnonymousUser': AnonymousUser.id
        }
        return super(LoginUserView, self).get_context_data(**kwargs)

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


