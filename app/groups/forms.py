from django import forms
from django.contrib.auth.models import User
from friendship.models import Friend

from .models import Group, GroupMembership


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


class ChangeOwnershipForm(forms.Form):
    members = forms.ChoiceField(widget=forms.RadioSelect, label='Change owner to')

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super(ChangeOwnershipForm, self).__init__(*args, **kwargs)

        users_list = self.group.groupmembership_set.exclude(
                user=self.group.created_by).filter(status=1).values_list('user_id',
                'user__username')

        self.fields['members'].choices = users_list

    def clean_members(self):
        user = None

        try:
            user_id = self.cleaned_data.get('members')
            user = self.group.groupmembership_set.get(user_id=user_id, status=1).user
        except:
            raise forms.ValidationError('User cannot be added as an owner')
        return user
