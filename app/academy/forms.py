from django import forms
from django.contrib.auth.models import User

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('created_at')

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['admin'].queryset = User.objects.filter(groups__name='Professor')


    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Course.objects.filter(name=name).exists():
            raise forms.ValidationError('Course with name %s is already taken. \
                    Please choose another one' % name)
        return name



class CourseProfessorForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('created_at', 'admin')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Course.objects.filter(name=name).exists():
            raise forms.ValidationError('Course with name %s is already taken. \
                    Please choose another one' % name)
        return name
