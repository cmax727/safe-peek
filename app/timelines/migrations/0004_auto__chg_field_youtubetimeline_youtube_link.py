# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'YoutubeTimeline.youtube_link'
        db.alter_column('timelines_youtubetimeline', 'youtube_link', self.gf('app.timelines.fields.YoutubeUrlField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'YoutubeTimeline.youtube_link'
        db.alter_column('timelines_youtubetimeline', 'youtube_link', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'timelines.filetimeline': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'FileTimeline', '_ormbases': ['timelines.Timeline']},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'})
        },
        'timelines.imagetimeline': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'ImageTimeline', '_ormbases': ['timelines.Timeline']},
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'})
        },
        'timelines.texttimeline': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'TextTimeline', '_ormbases': ['timelines.Timeline']},
            'content': ('django.db.models.fields.TextField', [], {}),
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'})
        },
        'timelines.timeline': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Timeline'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'timelines.youtubetimeline': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'YoutubeTimeline', '_ormbases': ['timelines.Timeline']},
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'}),
            'youtube_link': ('app.timelines.fields.YoutubeUrlField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['timelines']