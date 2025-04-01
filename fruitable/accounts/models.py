"""Custom user model"""
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# models.py

email_regex = RegexValidator(
  regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
  message="Please enter valid Email address.")
string_regex =  RegexValidator(
  regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$',
  message="Some special characters like (~!#^`'$|{}<>*) are not allowed.")
mobile_validate = RegexValidator(
  regex=r'^(\+\d{1,3})?\d{10}$',
  message='Enter a valid 10-digit mobile number +254 9999999999')


class CustomUser(AbstractUser):
    """Custom user model"""
    email = models.EmailField(unique=True, db_index=True, validators=[email_regex])
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True, validators=[string_regex])
    last_name = models.CharField(max_length=50, blank=True, null=True, validators=[string_regex])
    phone_number = models.CharField(
      max_length=10,
      blank=True, null=True, validators=[mobile_validate])

    def __str__(self):
        return self.email
