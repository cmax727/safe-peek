from django import forms
from .models import Profile, Status, CommentStatus
from django.contrib.auth.models import User
from app.academy.models import University
#from app.academy.forms import EventForm
from django.utils.translation import ugettext_lazy as _


class UserListForm(forms.Form):
    username = forms.ModelChoiceField(queryset=User.objects.all())
    university = forms.ModelChoiceField(queryset=University.objects.all())


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

    username = forms.CharField(label=_('Username'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    location = forms.CharField(label=_('Location'))
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['username', 'first_name', 'last_name', 'location',
                'gender', 'picture', 'user']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        exclude = ('created_by', 'created_at')


class CommentStatusForm(forms.ModelForm):
    class Meta:
        model = CommentStatus
        exclude = ('status', 'created_by', 'created_at')
