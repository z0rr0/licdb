# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Student'
        db.create_table('eis_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('who', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('eis', ['Student'])


    def backwards(self, orm):
        
        # Deleting model 'Student'
        db.delete_table('eis_student')


    models = {
        'eis.student': {
            'Meta': {'object_name': 'Student'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'})
        }
    }

    complete_apps = ['eis']
