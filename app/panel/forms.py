from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
#from registration.signals import user_registered


class UserRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label=_('First Name'), max_length=30)
    last_name = forms.CharField(label=_('Last Name'), max_length=30)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    # def clean_email(self):
    #     data = self.cleaned_data
    #     try:
    #         User.objects.filter(email=data['email'])
    #     except User.DoesNotExist:
    #         return data['email']
    #     raise forms.ValidationError('Email is already taken.')
