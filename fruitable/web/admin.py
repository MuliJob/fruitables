from django.contrib import admin
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django_ckeditor_5.fields import CKEditor5Widget

from .models import Cart, CartItem, Product, Subscriber, EmailTemplate



class EmailTemplateAdminForm(forms.ModelForm):
    """Email Template Admin"""
    class Meta:
        """Class meta"""
        model = EmailTemplate
        fields = '__all__'
        widgets = {
            'message': CKEditor5Widget(),
        }


class EmailTemplateAdmin(admin.ModelAdmin):
    """Admin template"""
    form = EmailTemplateAdminForm

    def save_model(self, request, obj, form, change):
        """Saving details to model"""
        super().save_model(request, obj, form, change)
        subject = obj.subject
        html_message = obj.message

        recipients = [subscriber.email for subscriber in obj.recipients.all()]
        from_email = settings.EMAIL_HOST_USER
        send_mail(
            subject,
            "",
            from_email,
            recipients,
            fail_silently=False,
            html_message=html_message
        )

# Register your models here.
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Subscriber)

admin.site.register(EmailTemplate,  EmailTemplateAdmin)