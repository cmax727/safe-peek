from django import forms
from django.contrib.auth.models import User
from app.academy.models import University
from app.events.forms import EventForm
from django.utils.translation import ugettext_lazy as _

from .models import Profile, Status, CommentStatus, Interest, Hobby


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

    def clean_username(self):
        if  self.instance.pk:
            q = User.objects.filter(
                username=self.cleaned_data['username']
            ).exclude(id=self.instance.pk)
            if q:
                raise forms.ValidationError(_('User with the same username already exists'))
        return self.cleaned_data['username']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'about_me', 'username',
            'first_name', 'last_name',
            'location', 'gender',
            'relationsheep', 'birth_date',
            'interests', 'hobbies',
            'picture', 'user']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        exclude = ('created_by', 'created_at')


class CommentStatusForm(forms.ModelForm):
    class Meta:
        model = CommentStatus
        exclude = ('status', 'created_by', 'created_at')


class PersonalEventForm(EventForm):
    event = forms.ChoiceField(widget=forms.HiddenInput())


class InterestForm(forms.ModelForm):

    def save(self, commit=True, **kwargs):
        qs = Interest.objects.filter(title__iexact=self.cleaned_data['title'])
        if qs:
            return qs[0]
        return super(InterestForm, self).save(commit, **kwargs)

    class Meta:
        model = Interest

class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
