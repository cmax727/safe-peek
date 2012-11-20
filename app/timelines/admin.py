from django.contrib import admin
from .models import Timeline, TextTimeline, ImageTimeline, YoutubeTimeline, FileTimeline


admin.site.register(Timeline)
admin.site.register(TextTimeline)
admin.site.register(ImageTimeline)
admin.site.register(YoutubeTimeline)
admin.site.register(FileTimeline)