from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import (
    LoginView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView)

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm, 
    CustomLoginForm, 
    EmailValidationOnForgotPassword,
    PasswordConfirmationForm)
from users.models import CustomUser

"""
    [Source]
    https://docs.djangoproject.com/en/3.1/topics/auth/default/#django.contrib.auth.views.PasswordChangeView
"""
class LoginUserView(LoginView):
    template_name = 'account/login.html'
    form_class  = CustomLoginForm

class SignUpView(CreateView):
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

class UpdateAccountView(UpdateView):
    template_name = 'account/update.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('share:index')
    queryset = CustomUser.objects.all()


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(form)
        return super(UpdateAccountView, self).post(request, *args, **kwargs)
    
class ResetPassWord(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = EmailValidationOnForgotPassword
    success_url= reverse_lazy('users:password_reset_done')
    email_template_name = 'account/resets_template/password_reset_email.html'
    # extra_context = 'Dict'

class ResetPassWordDone(PasswordResetDoneView):
    template_name= 'account/password_reset_done.html'
    # extra_context = 'Dict'

class ResetPassWordConfirmation(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm_new.html'
    form_class = PasswordConfirmationForm
    success_url = reverse_lazy('users:password_reset_complete')
    post_reset_login = True #A boolean indicating if the user should be automatically authenticated after a successful password reset
    # extra_context = 'Dict'

class ResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
    # extra_context = 'Dict'