from django import forms
from django.contrib.auth.models import User
#from app.panel.models import UserAvatar
#from registration.signals import user_registered
attrs_dict = {'class': 'required'}


class RegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=(u'password (again)'))

    # class Meta:
    #     model = UserAvatar
    #     exclude = ('User')

    def clean_username(self):
        data = self.cleaned_data
        try:
            User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError('This username is already taken.')

    def clean_email(self):
        data = self.cleaned_data
        if data['email'].count(".edu") > 0:
            return data['email']
        else:
            raise forms.ValidationError('Your email must using .edu')

        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return data['email']
        raise forms.ValidationError('This email is already taken.')

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError((u'You must type the same password each time'))
        return self.cleaned_data


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    #email = forms.EmailField()
    #avatar = forms.ImageField()

    # def __init__(self, *args, **kwargs):
    #     super(SignupForm, self).__init__(*args, **kwargs)
    #     print '######################waks#########################'
    #     self.fields.keyOrder = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        #user.email = self.cleaned_data['email']
        print user.email
        user.save()

    # def clean_email(self):
    #     print '######################blah#########################'
    #     data = self.cleaned_data
    #     if data['email'].count(".edu") > 0:
    #         return data['email']
    #     else:
    #         raise forms.ValidationError('Your email must using .edu')
