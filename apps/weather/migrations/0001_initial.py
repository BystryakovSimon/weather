# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table('weather_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('flag_small', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('flag_big', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('capital_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('weather', ['Region'])

        # Adding model 'Town'
        db.create_table('weather_town', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('flag_small', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('flag_big', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('geo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_towns', to=orm['weather.Region'])),
        ))
        db.send_create_signal('weather', ['Town'])

        # Adding model 'MeteoCenter'
        db.create_table('weather_meteocenter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('flag', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('xml', self.gf('django.db.models.fields.TextField')()),
            ('f_timestep', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('s_timestep', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('date_tag', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('date_reg', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('weather', ['MeteoCenter'])

        # Adding model 'Town_MeteoCenter'
        db.create_table('weather_town_meteocenter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_meteocenters', to=orm['weather.Town'])),
            ('meteocenter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_t_m', to=orm['weather.MeteoCenter'])),
            ('id_of_town', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_date_f', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('meteo_town_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('weather', ['Town_MeteoCenter'])

        # Adding model 'TimeUpdate'
        db.create_table('weather_timeupdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meteocenter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_tu', to=orm['weather.MeteoCenter'])),
            ('time_update', self.gf('django.db.models.fields.TimeField')()),
            ('time_indent', self.gf('django.db.models.fields.TimeField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('weather', ['TimeUpdate'])

        # Adding model 'GeneralHashtag'
        db.create_table('weather_generalhashtag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('g_hashtag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('weather', ['GeneralHashtag'])

        # Adding model 'ProvideData'
        db.create_table('weather_providedata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meteocenter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_gm_hashtags', to=orm['weather.MeteoCenter'])),
            ('g_hashtag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_mc_hashtags', to=orm['weather.GeneralHashtag'])),
            ('m_hashtag', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('s_timestep', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_hashtag_attr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('m_hashtag_desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('weather', ['ProvideData'])

        # Adding model 'WData'
        db.create_table('weather_wdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('town_meteo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_datas_by_tm', to=orm['weather.Town_MeteoCenter'])),
            ('time', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_datas_by_tu', to=orm['weather.TimeUpdate'])),
            ('g_hashtag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_datas_by_gh', to=orm['weather.GeneralHashtag'])),
            ('date_f', self.gf('django.db.models.fields.DateTimeField')()),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('d_data_upd', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 28, 0, 0))),
        ))
        db.send_create_signal('weather', ['WData'])

        # Adding model 'WLog'
        db.create_table('weather_wlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_record', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 28, 0, 0))),
            ('town_meteo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_wlogs_by_tm', to=orm['weather.Town_MeteoCenter'])),
            ('time_update_meteo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_wlogs_by_tu', to=orm['weather.TimeUpdate'])),
            ('meteo_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('weather', ['WLog'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table('weather_region')

        # Deleting model 'Town'
        db.delete_table('weather_town')

        # Deleting model 'MeteoCenter'
        db.delete_table('weather_meteocenter')

        # Deleting model 'Town_MeteoCenter'
        db.delete_table('weather_town_meteocenter')

        # Deleting model 'TimeUpdate'
        db.delete_table('weather_timeupdate')

        # Deleting model 'GeneralHashtag'
        db.delete_table('weather_generalhashtag')

        # Deleting model 'ProvideData'
        db.delete_table('weather_providedata')

        # Deleting model 'WData'
        db.delete_table('weather_wdata')

        # Deleting model 'WLog'
        db.delete_table('weather_wlog')


    models = {
        'weather.generalhashtag': {
            'Meta': {'ordering': "['id']", 'object_name': 'GeneralHashtag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'g_hashtag': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'weather.meteocenter': {
            'Meta': {'ordering': "['id']", 'object_name': 'MeteoCenter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_reg': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_tag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'f_timestep': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'flag': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            's_timestep': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'xml': ('django.db.models.fields.TextField', [], {})
        },
        'weather.providedata': {
            'Meta': {'ordering': "['meteocenter']", 'object_name': 'ProvideData'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'g_hashtag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_mc_hashtags'", 'to': "orm['weather.GeneralHashtag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm_hashtag': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'm_hashtag_attr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'm_hashtag_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_gm_hashtags'", 'to': "orm['weather.MeteoCenter']"}),
            's_timestep': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'weather.region': {
            'Meta': {'ordering': "['id']", 'object_name': 'Region'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'capital_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flag_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'flag_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'weather.timeupdate': {
            'Meta': {'ordering': "['id']", 'object_name': 'TimeUpdate'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_tu'", 'to': "orm['weather.MeteoCenter']"}),
            'time_indent': ('django.db.models.fields.TimeField', [], {}),
            'time_update': ('django.db.models.fields.TimeField', [], {})
        },
        'weather.town': {
            'Meta': {'ordering': "['id']", 'object_name': 'Town'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'flag_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'flag_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'geo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_towns'", 'to': "orm['weather.Region']"})
        },
        'weather.town_meteocenter': {
            'Meta': {'ordering': "['id']", 'object_name': 'Town_MeteoCenter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_of_town': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_date_f': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meteo_town_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_t_m'", 'to': "orm['weather.MeteoCenter']"}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_meteocenters'", 'to': "orm['weather.Town']"})
        },
        'weather.wdata': {
            'Meta': {'ordering': "['-id']", 'object_name': 'WData'},
            'd_data_upd': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 28, 0, 0)'}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_f': ('django.db.models.fields.DateTimeField', [], {}),
            'g_hashtag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_datas_by_gh'", 'to': "orm['weather.GeneralHashtag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_datas_by_tu'", 'to': "orm['weather.TimeUpdate']"}),
            'town_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_datas_by_tm'", 'to': "orm['weather.Town_MeteoCenter']"})
        },
        'weather.wlog': {
            'Meta': {'ordering': "['-id']", 'object_name': 'WLog'},
            'data_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_record': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 28, 0, 0)'}),
            'error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meteo_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_update_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_wlogs_by_tu'", 'to': "orm['weather.TimeUpdate']"}),
            'town_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_wlogs_by_tm'", 'to': "orm['weather.Town_MeteoCenter']"})
        }
    }

    complete_apps = ['weather']