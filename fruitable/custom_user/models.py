"""User model"""
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    """User model"""
    objects = BaseUserManager()
