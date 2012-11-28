from django import forms
from django.contrib.auth.models import User

from .models import Course, CourseFiles, University, Syllabus, Assignment, AssignmentSubmit

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


class UniversityAdminForm(forms.Form):
    admins = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        university = kwargs.pop('university', '')
        super(UniversityAdminForm, self).__init__(*args, **kwargs)
        members = university.members.all()
        current_admins = []

        for membership in university.academy_roles.all():
            if membership.role == 3 and membership.user.pk not in current_admins:
                current_admins.append(membership.user.pk)
        self.fields['admins'].choices = [(u.pk, u.display_name()) for u in members]
        self.fields['admins'].initial = current_admins


class UniversityProfessorForm(forms.Form):
    professors = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        university = kwargs.pop('university', '')
        super(UniversityProfessorForm, self).__init__(*args, **kwargs)
        members = university.members.all()
        current_professors = []

        for membership in university.academy_roles.all():
            if membership.role == 2 and membership.user.pk not in current_professors:
                current_professors.append(membership.user.pk)

        self.fields['professors'].choices = [(u.pk, u.display_name()) for u in members]
        self.fields['professors'].initial = current_professors


class UniversityCourseForm(forms.ModelForm):
    university = forms.ModelChoiceField(queryset=University.objects.all(), widget=forms.HiddenInput())
    professors = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    students = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Course
        exclude = ('created_at', 'members')

    def __init__(self, *args, **kwargs):
        university_obj = kwargs.pop('university', '')
        super(UniversityCourseForm, self).__init__(*args, **kwargs)
        self.fields['university'].initial = university_obj
        self.fields['professor'].queryset = university_obj.members.\
                filter(academy_roles__role=2, academy_roles__university=university_obj)
        self.fields['students'].queryset = university_obj.members.filter(academy_roles__role=1)


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


class CourseFilesForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CourseFiles
        exclude = ('created_at')


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


class AssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Assignment
        exclude = ('created_at', 'members')


class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmit
        exclude = ('user', 'grade', 'assignment')
