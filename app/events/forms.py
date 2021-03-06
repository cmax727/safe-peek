from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Event


class EventForm(forms.ModelForm):
    event = forms.ChoiceField(help_text='Share status on your event / your groups')

    class Meta:
        model = Event
        exclude = ('created_by', 'content_type', 'object_id')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EventForm, self).__init__(*args, **kwargs)

        allowed_postings = self.user.active_groups()
        allowed_postings.insert(0, self.user.profile)
        allowed_postings.extend(self.user.active_courses())
        allowed_postings.extend(self.user.university_set.all())
        event_choices = []

        for instance in allowed_postings:
            ctype = ContentType.objects.get_for_model(instance)
            ctype_object = '%s_%s' % (ctype.pk, instance.pk)
            event_choices.append((ctype_object, instance))

        self.fields['event'].choices = event_choices

    def clean_timeline(self):
        data = self.cleaned_data.get('event', '')
        ctype_pk, object_id = data.split('_')

        try:
            ctype = ContentType.objects.get_for_id(ctype_pk)
            # below line will raise error if the object doesn't exist
            ctype.model_class().objects.get(pk=object_id)
        except:
            raise forms.ValidationError('You can not send update to that event')
        return data

    def save(self, force_insert=False, force_update=False, commit=True):
        data = self.cleaned_data.pop('event')
        obj = super(EventForm, self).save(commit=False)

        ctype_pk, object_id = data.split('_')
        obj.content_type_id = ctype_pk
        obj.object_id = object_id
        return obj
