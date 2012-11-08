from django import forms
from app.panel.models import UserProfile

#from registration.signals import user_registered


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    #avatar = forms.ImageField()

    class Meta:
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        #self.fields.keyOrder = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

    # def clean_email(self):
    #     data = self.cleaned_data
    #     try:
    #         User.objects.filter(email=data['email'])
    #     except User.DoesNotExist:
    #         return data['email']
    #     raise forms.ValidationError('Email is already taken.')
