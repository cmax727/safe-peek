from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import TextTimeline, ImageTimeline, YoutubeTimeline, FileTimeline


class TimelineBaseForm(forms.ModelForm):
    timeline = forms.ChoiceField(help_text='Share status on your timeline / your groups')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TimelineBaseForm, self).__init__(*args, **kwargs)

        allowed_postings = self.user.active_groups()
        allowed_postings.insert(0, self.user.profile)
        # allowed_postings2 = self.user.active_course()
        # allowed_postings.insert(0, self.user.user_university())

        timeline_choices = []

        for instance in allowed_postings:
            ctype = ContentType.objects.get_for_model(instance.__class__)
            ctype_object = '%s_%s' % (ctype.pk, instance.pk)
            timeline_choices.append((ctype_object, instance))

        # for instance2 in allowed_postings2:
        #     ctype2 = ContentType.objects.get_for_model(instance.__class__)
        #     ctype_object2 = '%s_%s' % (ctype2.pk, instance2.pk)
        #     timeline_choices.append((ctype_object2, instance2))

        self.fields['timeline'].choices = timeline_choices

    def clean_timeline(self):
        data = self.cleaned_data.get('timeline', '')
        ctype_pk, object_id = data.split('_')

        try:
            ctype = ContentType.objects.get_for_id(ctype_pk)
            # below line will raise error if the object doesn't exist
            ctype.model_class().objects.get(pk=object_id)
        except:
            raise forms.ValidationError('You can not send update to that timeline')
        return data

    def save(self, force_insert=False, force_update=False, commit=True):
        data = self.cleaned_data.pop('timeline')
        obj = super(TimelineBaseForm, self).save(commit=False)

        ctype_pk, object_id = data.split('_')
        obj.content_type_id = ctype_pk
        obj.object_id = object_id
        return obj


class TextTimelineForm(TimelineBaseForm):
    class Meta:
        model = TextTimeline
        exclude = ('created_by', 'content_type', 'object_id')


class ImageTimelineForm(TimelineBaseForm):

    class Meta:
        exclude = ('created_by', 'content_type', 'object_id')
        model = ImageTimeline


class YoutubeTimelineForm(TimelineBaseForm):
    class Meta:
        model = YoutubeTimeline
        exclude = ('created_by', 'content_type', 'object_id')


class FileTimelineForm(TimelineBaseForm):
    class Meta:
        model = FileTimeline
        exclude = ('created_by', 'content_type', 'object_id')
