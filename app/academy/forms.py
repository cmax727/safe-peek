from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .models import Course, University, Syllabus

import re


class UniversityForm(forms.ModelForm):
    domain = forms.CharField(max_length=50, help_text='All registered users within the same domain will be registered as students of the university')

    class Meta:
        model = University
        exclude = ('slug', 'members')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if University.objects.filter(name=name).exists():
            raise forms.ValidationError('University with name %s is already taken. \
                    Please choose another one' % name)
        return name

    def clean_domain(self):
        domain = self.cleaned_data.get('domain')
        domain_pattern = '^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$'

        if not re.search(domain_pattern, domain):
            raise forms.ValidationError('Invalid domain name')
        return domain

    def save(self, force_insert=False, force_update=False, commit=True):
        obj = super(UniversityForm, self).save(commit=False)

        if commit:
            obj.slug = slugify(obj.name)
            obj.save()
        return obj


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('created_at')

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['professor'].queryset = User.objects.filter(profile__user_type=2)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Course.objects.filter(name=name).exists():
            raise forms.ValidationError('Course with name %s is already taken. \
                    Please choose another one' % name)
        return name


class CourseProfessorForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('created_at', 'professor')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Course.objects.filter(name=name).exists():
            raise forms.ValidationError('Course with name %s is already taken. \
                    Please choose another one' % name)
        return name


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        exclude = ('created_at', 'course')
