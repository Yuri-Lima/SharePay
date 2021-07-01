from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm)
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from .models import CustomUser

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
            }),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password confirmation',
                }),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser  
        fields = ('username', 'email','password1','password2')
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
        }

    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password',
            }),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'new-password',
                'placeholder': 'Enter password confirmation',
                }),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )

