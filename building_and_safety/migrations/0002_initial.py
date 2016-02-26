# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FireAlarm'
        db.create_table(u'building_and_safety_firealarm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance_no', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('alarm_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('building_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('repeat_cnt', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('longtitude_x', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('latitude_y', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('activation_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('activation_month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('activation_day', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('activation_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time_of_the_day', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('in_holiday', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rainfall', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('true_or_false_alarm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('building_and_safety', ['FireAlarm'])

        # Adding model 'Features'
        db.create_table(u'building_and_safety_features', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature_name', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('feature_desc', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal('building_and_safety', ['Features'])


    def backwards(self, orm):
        # Deleting model 'FireAlarm'
        db.delete_table(u'building_and_safety_firealarm')

        # Deleting model 'Features'
        db.delete_table(u'building_and_safety_features')


    models = {
        'building_and_safety.features': {
            'Meta': {'object_name': 'Features'},
            'feature_desc': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'feature_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'building_and_safety.firealarm': {
            'Meta': {'ordering': "('-activation_year', '-activation_month', '-activation_day', '-activation_day')", 'unique_together': '()', 'object_name': 'FireAlarm', 'index_together': '()'},
            'activation_day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'activation_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'activation_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'activation_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'alarm_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'building_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_holiday': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'instance_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'latitude_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longtitude_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rainfall': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'repeat_cnt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'time_of_the_day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'true_or_false_alarm': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['building_and_safety']