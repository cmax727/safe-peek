# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Timeline'
        db.create_table('timelines_timeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('timelines', ['Timeline'])

        # Adding model 'TextTimeline'
        db.create_table('timelines_texttimeline', (
            ('timeline_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['timelines.Timeline'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('timelines', ['TextTimeline'])

        # Adding model 'ImageTimeline'
        db.create_table('timelines_imagetimeline', (
            ('timeline_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['timelines.Timeline'], unique=True, primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('timelines', ['ImageTimeline'])

        # Adding model 'YoutubeTimeline'
        db.create_table('timelines_youtubetimeline', (
            ('timeline_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['timelines.Timeline'], unique=True, primary_key=True)),
            ('youtube_link', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('timelines', ['YoutubeTimeline'])

        # Adding model 'FileTimeline'
        db.create_table('timelines_filetimeline', (
            ('timeline_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['timelines.Timeline'], unique=True, primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('timelines', ['FileTimeline'])


    def backwards(self, orm):
        # Deleting model 'Timeline'
        db.delete_table('timelines_timeline')

        # Deleting model 'TextTimeline'
        db.delete_table('timelines_texttimeline')

        # Deleting model 'ImageTimeline'
        db.delete_table('timelines_imagetimeline')

        # Deleting model 'YoutubeTimeline'
        db.delete_table('timelines_youtubetimeline')

        # Deleting model 'FileTimeline'
        db.delete_table('timelines_filetimeline')


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
            'Meta': {'object_name': 'FileTimeline', '_ormbases': ['timelines.Timeline']},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'})
        },
        'timelines.imagetimeline': {
            'Meta': {'object_name': 'ImageTimeline', '_ormbases': ['timelines.Timeline']},
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'})
        },
        'timelines.texttimeline': {
            'Meta': {'object_name': 'TextTimeline', '_ormbases': ['timelines.Timeline']},
            'content': ('django.db.models.fields.TextField', [], {}),
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'})
        },
        'timelines.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'timelines.youtubetimeline': {
            'Meta': {'object_name': 'YoutubeTimeline', '_ormbases': ['timelines.Timeline']},
            'timeline_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['timelines.Timeline']", 'unique': 'True', 'primary_key': 'True'}),
            'youtube_link': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['timelines']