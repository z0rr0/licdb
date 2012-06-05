# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Key', fields ['use']
        db.create_index('key_key', ['use'])

        # Adding index on 'Key', fields ['date_end']
        db.create_index('key_key', ['date_end'])

        # Adding index on 'Key', fields ['date_start']
        db.create_index('key_key', ['date_start'])

        # Adding index on 'Key', fields ['net']
        db.create_index('key_key', ['net'])

        # Adding index on 'License', fields ['free']
        db.create_index('key_license', ['free'])

        # Adding index on 'Client', fields ['student']
        db.create_index('key_client', ['student'])

        # Adding index on 'Client', fields ['date_start']
        db.create_index('key_client', ['date_start'])

        # Adding index on 'Client', fields ['manyuse']
        db.create_index('key_client', ['manyuse'])

        # Adding index on 'Client', fields ['name']
        db.create_index('key_client', ['name'])


    def backwards(self, orm):
        
        # Removing index on 'Client', fields ['name']
        db.delete_index('key_client', ['name'])

        # Removing index on 'Client', fields ['manyuse']
        db.delete_index('key_client', ['manyuse'])

        # Removing index on 'Client', fields ['date_start']
        db.delete_index('key_client', ['date_start'])

        # Removing index on 'Client', fields ['student']
        db.delete_index('key_client', ['student'])

        # Removing index on 'License', fields ['free']
        db.delete_index('key_license', ['free'])

        # Removing index on 'Key', fields ['net']
        db.delete_index('key_key', ['net'])

        # Removing index on 'Key', fields ['date_start']
        db.delete_index('key_key', ['date_start'])

        # Removing index on 'Key', fields ['date_end']
        db.delete_index('key_key', ['date_end'])

        # Removing index on 'Key', fields ['use']
        db.delete_index('key_key', ['use'])


    models = {
        'key.client': {
            'Meta': {'ordering': "['student', 'name', 'key__program__name']", 'object_name': 'Client'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['key.Key']"}),
            'manyuse': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_index': 'True'}),
            'student': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'key.key': {
            'Meta': {'ordering': "['use', 'program__name', 'id']", 'object_name': 'Key'},
            'attach': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 6, 5, 15, 51, 22, 400912)', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'manyuse': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'net': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['key.Program']"}),
            'use': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'})
        },
        'key.license': {
            'Meta': {'ordering': "['name']", 'object_name': 'License'},
            'attach': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '127'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'key.program': {
            'Meta': {'ordering': "['name']", 'object_name': 'Program'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['key.License']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'use_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['key']
