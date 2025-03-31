"""Application forms"""
from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from .models import Review, Subscriber


class ReviewForm(forms.ModelForm):
    """Review form"""
    class Meta:
        '''Class Meta'''
        model = Review
        fields = ['email', 'name', 'description', 'star']

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


class SubscriberForm(forms.ModelForm):
    """Subscriber Model"""
    class Meta:
        '''Class Meta'''
        model = Subscriber
        fields = ['email']
