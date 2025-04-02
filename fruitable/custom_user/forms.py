"""Login and register form"""
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


from .models import User


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    """Register form"""
    class Meta:
        """Class meta"""
        model = User
        fields = ['email', 'password1', 'password2']


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):
    """Login form"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
