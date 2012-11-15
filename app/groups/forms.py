from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend

from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('created_by', 'created_at')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(GroupForm, self).__init__(*args, **kwargs)

        friends = Friend.objects.friends(user)
        friends_pks = [u.pk for u in friends]

        if len(friends_pks) < 1:
            friends = User.objects.none()

        else:
            friends = User.objects.filter(pk__in=friends_pks)
        self.fields['members'].queryset = friends

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Group.objects.filter(name=name).exists():
            raise forms.ValidationError('Group with name %s is already taken. \
                    Please choose another one' % name)
        return name
