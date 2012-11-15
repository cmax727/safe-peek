from django import forms
from .models import Profile, Status
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

    username = forms.CharField(label=_('Username'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username', 'first_name', 'last_name',
                'gender', 'picture', 'user']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
