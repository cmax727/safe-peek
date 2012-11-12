from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, ugettext


class SignupForm(forms.Form):

    def save(self, user):
        data = self.cleaned_data
        email = data.get("email", "asal")

        if not email.endswith('.edu'):
            raise forms.ValidationError(_('You must use .edu email'))

        super(SignupForm, self).save(user)