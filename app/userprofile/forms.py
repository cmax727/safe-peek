from django import forms
from models import Profile, Status
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user')


class NameForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('username', 'email', 'password', 'is_staff', 'is_active',
            'is_superuser', 'date_joined', 'groups', 'last_login', 'user_permissions')
    # first_name = forms.CharField(label=_('First Name'), max_length=30)
    # last_name = forms.CharField(label=_('Last Name'), max_length=30)


class SignupForm(forms.Form):

    def save(self, user):
        data = self.cleaned_data
        email = data.get("email", "asal")

        if not email.endswith('.edu'):
            raise forms.ValidationError(_('You must use .edu email'))

        super(SignupForm, self).save(user)


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
