from django import forms
from models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('created_by', 'created_date')
