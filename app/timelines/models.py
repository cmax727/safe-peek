from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from .fields import YoutubeUrlField

import os


class Timeline(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('timelines:detail', [str(self.pk)])

    def get_type(self):
        if hasattr(self, 'texttimeline'):
            return 'text'
        elif hasattr(self, 'imagetimeline'):
            return 'image'
        elif hasattr(self, 'youtubetimeline'):
            return 'youtube'
        elif hasattr(self, 'filetimeline'):
            return 'file'
        else:
            return None

    def get_content(self):
        if hasattr(self, 'texttimeline'):
            return self.texttimeline
        elif hasattr(self, 'imagetimeline'):
            return self.imagetimeline
        elif hasattr(self, 'youtubetimeline'):
            return self.youtubetimeline
        elif hasattr(self, 'filetimeline'):
            return self.filetimeline
        else:
            return None


class TextTimeline(Timeline):
    content = models.TextField()


class ImageTimeline(Timeline):
    image = models.ImageField(upload_to='timelines')
    thumbnail_image = ImageSpecField([ResizeToFit(302, None)],
            image_field='image',
            format='JPEG',
            options={'quality': 90})


class YoutubeTimeline(Timeline):
    youtube_link = YoutubeUrlField()


class FileTimeline(Timeline):
    attachment = models.FileField(upload_to='timelines')

    @property
    def filename(self):
        res = 'Download file'
        try:
            res = os.path.basename(self.attachment.name)
        except:
            pass
        return res
