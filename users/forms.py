from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,)
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from .models import CustomUser
from allauth.account.forms import (
    LoginForm,
    SignupForm,
    AddEmailForm,
    ChangePasswordForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    
)
from allauth.socialaccount.forms import (
    SignupForm as SignupFormSocial,
    DisconnectForm,
)

from allauth import app_settings
from django.utils.translation import gettext, gettext_lazy as _, pgettext
from allauth.utils import (
    get_username_max_length,
    set_form_field_order
    )


class CustomLoginAccount(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginAccount, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'current-password',
                'id': 'pwd1',
                "type": "password",
                'label': _("Password"),
                'autocomplete': "current-password",
                'placeholder': 'Enter password',
            }
        )
        self.fields['login'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
            }
        )

    def clean(self):
        print(self.cleaned_data)
        return super(CustomLoginAccount,self).clean()

class CustomSignupAccount(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupAccount, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                "placeholder": _("Username"), 
                "autocomplete": "username",
                'autofocus': 'True',
                'class': 'form-control',
                'aria-label': 'Enter username...',
                'aria-describedby':'submit-username',
            }
        )
        self.fields['email'].widget = forms.PasswordInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
                'autofocus': 'True',
                'class': 'form-control',
                'aria-label': 'Enter email...',
                'aria-describedby':'submit-email',
            }
        )
        self.fields['password1'].widget = forms.TextInput(
            attrs={
                'id': 'pwd1',
                "placeholder": _("Password"), 
                'autofocus': 'True',
                'autocomplete': 'new-password',
                'class': 'form-control',
                'type':"password"
            }
        )
        self.fields['password2'].widget = forms.TextInput(
            attrs={
                'id': 'pwd2',
                "placeholder": _("Password Again"), 
                'autofocus': 'True',
                'autocomplete': 'new-password',
                'class': 'form-control',
                'type':"password"
            }
        )

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupAccount, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

class CustomAddEmailAccount(AddEmailForm):
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                'autofocus': True,
                'class': 'form-control',
                "placeholder": _("E-mail address"),
                'aria-label': 'Enter email...',
                'aria-describedby':'submit-email',
            }
        ),
    )
    def save(self):

        # Ensure you call the parent class's save.
        # .save() returns an allauth.account.models.EmailAddress object.
        email_address_obj = super(CustomAddEmailAccount, self).save()

        # Add your own processing here.

        # You must return the original result.
        return email_address_obj

class ChangePasswordFormAccount(ChangePasswordForm):
    def save(self):

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(ChangePasswordFormAccount, self).save()

class SetPasswordFormAccount(SetPasswordForm):
    def save(self):

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(SetPasswordFormAccount, self).save()

        # Add your own processing here.

class ResetPasswordFormAccount(ResetPasswordForm):
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
                'autofocus': 'True',
                'class': 'form-control',
                'aria-label': 'Enter email...',
                'aria-describedby':'submit-email',
            }
        ),
    )

class ResetPasswordKeyFormAccount(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyFormAccount, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.TextInput(
            attrs={
                'id': 'pwd1',
                "placeholder": _("Password"), 
                'autofocus': 'True',
                'autocomplete': 'new-password',
                'class': 'form-control',
                'type':"password"
            }
        )
        self.fields['password2'].widget = forms.TextInput(
            attrs={
                'id': 'pwd2',
                "placeholder": _("Password"), 
                'autofocus': 'True',
                'autocomplete': 'new-password',
                'class': 'form-control',
                'type':"password"
            }
        )


class SignupFormSocialAccount(SignupFormSocial):
    username = forms.CharField(
        label=_("Username"),
        # min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Username"), 
                "autocomplete": "username",
                'autofocus': 'True',
                'class': 'form-control',
                'aria-label': 'Enter username...',
                'aria-describedby':'submit-username',
            }
        ),
    )
    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
                'autofocus': 'True',
                'class': 'form-control',
                'aria-label': 'Enter email...',
                'aria-describedby':'submit-email',
            }
        ),
    )

class DisconnectFormAccount(DisconnectForm):
    def save(self):

        # Add your own processing here if you do need access to the
        # socialaccount being deleted.

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(DisconnectFormAccount, self).save()

        # Add your own processing here if you don't need access to the
        # socialaccount being deleted.







class PasswordConfirmationForm(SetPasswordForm):
    class Meta:
        help_texts = {
                'new_password2': None,
                'new_password1': None,
            }
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'autocomplete': 'new-password',
                'class': 'form-control',
                'placeholder': 'Enter password',
                }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password-confirmation',
                'class': 'form-control',
                'placeholder': 'Enter password confirmation',
                }),
    )

class EmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'autocomplete': 'email',
                'class': 'form-control',
                'placeholder': 'Your email here...',
                'aria-label': 'Enter email...',
                'aria-describedby':'submit-button',
            })
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email__iexact=email, is_active=True).exists():
            msg = ("This E-Mail address is not registered.")
            self.add_error('email', msg)
        return email

class CustomLoginForm(AuthenticationForm):
    
    username = forms.CharField(
        widget=TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Enter username...',
                'aria-label': 'Enter username...',
                'aria-describedby':'submit-button',
            }
        )
    )
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'current-password',
                'placeholder': 'Enter password',
                'type':"password",
            }
        )
    )

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'class': 'form-control',
                    'placeholder': 'Username or Email',
                    'aria-label': 'Username or Email',
                    'aria-describedby':'submit-button',
                }),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email...',
                    'aria-label': 'Enter email...',
                    'aria-describedby':'submit-button',
                }),
        }

    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password',
                'id':"pwd1",
                'type':"password"
            }),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password confirmation',
                'id':"pwd2",
                'type':"password"
                }),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    class Meta(UserChangeForm.Meta):
        model = CustomUser  
        fields = ('username', 'email', 'first_name', 'last_name' )
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'class': 'form-control',
                    'placeholder': 'Enter username...',
                    'aria-label': 'Enter username...',
                    'aria-describedby':'submit-button',
                }),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email...',
                    'aria-label': 'Enter email...',
                    'aria-describedby':'submit-button',
                }),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter First Name...',
                    'aria-label': 'Enter First Name......',
                    'aria-describedby':'submit-firstname',
                }),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Last Name...',
                    'aria-label': 'Enter Last Name......',
                    'aria-describedby':'submit-lastname',
                }),
        }

    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password',
            }),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password confirmation',
                }),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

