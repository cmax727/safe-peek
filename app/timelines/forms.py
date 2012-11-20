from django import forms
from .models import Timeline, TextTimeline, ImageTimeline, YoutubeTimeline, FileTimeline
from django.contrib.auth.models import User


class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        exclude = ('created_by, object_id, content_type')


class TextTimelineForm(forms.ModelForm):
    class Meta:
        model = TextTimeline
        exclude = ('created_by, object_id, content_type')


class ImageTimelineForm(forms.ModelForm):
    class Meta:
        model = ImageTimeline
        exclude = ('created_by, object_id, content_type')


class YoutubeTimelineForm(forms.ModelForm):
    class Meta:
        model = YoutubeTimeline
        exclude = ('created_by, object_id, content_type')


class FileTimelineForm(forms.ModelForm):
    class Meta:
        model = FileTimeline
        exclude = ('created_by, object_id, content_type')
