"""Application forms"""
from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from .models import Review


class ReviewForm(forms.ModelForm):
    """Review form"""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    description = forms.CharField(required=True)

    class Meta:
        '''Class Meta'''
        model = Review
        fields = ['email', 'name', 'description']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if email:
            try:
                EmailValidator()(email)
            except ValidationError as exc:
                raise forms.ValidationError(
                    {'email': "Please enter a valid email address."}) from exc

        if name and len(name) > 255:
            raise forms.ValidationError(
                {'name': "Name must not exceed a length 255 characters."})

        if description and len(description) > 1000:
            raise forms.ValidationError(
                {'description': "Description must not exceed a length 255 characters."})

        return cleaned_data
