from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import TextTimeline, ImageTimeline, YoutubeTimeline, FileTimeline


class TimelineBaseForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.all(), widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        obj = kwargs.pop('content_object')
        super(TimelineBaseForm, self).__init__(*args, **kwargs)

        ctype = ContentType.objects.get_for_model(obj.__class__)
        self.fields['content_type'].initial = ctype
        self.fields['object_id'].initial = obj.pk


class TextTimelineForm(TimelineBaseForm):
    class Meta:
        model = TextTimeline
        exclude = ('created_by',)


class ImageTimelineForm(TimelineBaseForm):

    class Meta:
        exclude = ('created_by',)
        model = ImageTimeline


class YoutubeTimelineForm(TimelineBaseForm):
    class Meta:
        model = YoutubeTimeline
        exclude = ('created_by',)


class FileTimelineForm(TimelineBaseForm):
    class Meta:
        model = FileTimeline
        exclude = ('created_by',)
