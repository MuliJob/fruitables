"""Login and register form"""
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


from .models import User


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    """Register form"""
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your password'}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}
        )
    )
    class Meta:
        """Class meta"""
        model = User
        fields = ['email', 'password1', 'password2']


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):
    """Login form"""
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
