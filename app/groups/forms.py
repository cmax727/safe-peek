from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('created_by', 'created_at')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Group.objects.filter(name=name).exists():
            raise forms.ValidationError('Group with name %s is already taken. \
                    Please choose another one' % name)
        return name
