# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table(u'weather_app_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('flag_small', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('flag_big', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('capital_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'weather_app', ['Region'])

        # Adding model 'Town'
        db.create_table(u'weather_app_town', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('town_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('flag_small', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('flag_big', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('geo', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_towns', to=orm['weather_app.Region'])),
        ))
        db.send_create_signal(u'weather_app', ['Town'])

        # Adding model 'MeteoCenter'
        db.create_table(u'weather_app_meteocenter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('showing_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
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
        db.send_create_signal(u'weather_app', ['MeteoCenter'])

        # Adding model 'Town_MeteoCenter'
        db.create_table(u'weather_app_town_meteocenter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_meteocenters', to=orm['weather_app.Town'])),
            ('meteocenter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_t_m', to=orm['weather_app.MeteoCenter'])),
            ('id_of_town', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_date_f', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('meteo_town_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('on_main', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'weather_app', ['Town_MeteoCenter'])

        # Adding model 'TimeUpdate'
        db.create_table(u'weather_app_timeupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meteocenter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_tu', to=orm['weather_app.MeteoCenter'])),
            ('time_update', self.gf('django.db.models.fields.TimeField')()),
            ('time_indent', self.gf('django.db.models.fields.TimeField')()),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'weather_app', ['TimeUpdate'])

        # Adding model 'GeneralHashtag'
        db.create_table(u'weather_app_generalhashtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('g_hashtag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'weather_app', ['GeneralHashtag'])

        # Adding model 'ProvideData'
        db.create_table(u'weather_app_providedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meteocenter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_gm_hashtags', to=orm['weather_app.MeteoCenter'])),
            ('g_hashtag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_mc_hashtags', to=orm['weather_app.GeneralHashtag'])),
            ('m_hashtag', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('s_timestep', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('m_hashtag_attr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('m_hashtag_desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'weather_app', ['ProvideData'])

        # Adding model 'WData'
        db.create_table(u'weather_app_wdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('town_meteo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_datas_by_tm', to=orm['weather_app.Town_MeteoCenter'])),
            ('time', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_datas_by_tu', to=orm['weather_app.TimeUpdate'])),
            ('g_hashtag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_datas_by_gh', to=orm['weather_app.GeneralHashtag'])),
            ('date_f', self.gf('django.db.models.fields.DateTimeField')()),
            ('data', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('d_data_upd', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 6, 2, 0, 0))),
        ))
        db.send_create_signal(u'weather_app', ['WData'])

        # Adding model 'WLog'
        db.create_table(u'weather_app_wlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_record', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 6, 2, 0, 0))),
            ('town_meteo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_wlogs_by_tm', to=orm['weather_app.Town_MeteoCenter'])),
            ('time_update_meteo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='get_wlogs_by_tu', to=orm['weather_app.TimeUpdate'])),
            ('meteo_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('data_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'weather_app', ['WLog'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table(u'weather_app_region')

        # Deleting model 'Town'
        db.delete_table(u'weather_app_town')

        # Deleting model 'MeteoCenter'
        db.delete_table(u'weather_app_meteocenter')

        # Deleting model 'Town_MeteoCenter'
        db.delete_table(u'weather_app_town_meteocenter')

        # Deleting model 'TimeUpdate'
        db.delete_table(u'weather_app_timeupdate')

        # Deleting model 'GeneralHashtag'
        db.delete_table(u'weather_app_generalhashtag')

        # Deleting model 'ProvideData'
        db.delete_table(u'weather_app_providedata')

        # Deleting model 'WData'
        db.delete_table(u'weather_app_wdata')

        # Deleting model 'WLog'
        db.delete_table(u'weather_app_wlog')


    models = {
        u'weather_app.generalhashtag': {
            'Meta': {'ordering': "['id']", 'object_name': 'GeneralHashtag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'g_hashtag': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'weather_app.meteocenter': {
            'Meta': {'ordering': "['id']", 'object_name': 'MeteoCenter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_reg': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_tag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'f_timestep': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'flag': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            's_timestep': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'showing_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'xml': ('django.db.models.fields.TextField', [], {})
        },
        u'weather_app.providedata': {
            'Meta': {'ordering': "['meteocenter']", 'object_name': 'ProvideData'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'g_hashtag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_mc_hashtags'", 'to': u"orm['weather_app.GeneralHashtag']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'm_hashtag': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'm_hashtag_attr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'm_hashtag_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_gm_hashtags'", 'to': u"orm['weather_app.MeteoCenter']"}),
            's_timestep': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'weather_app.region': {
            'Meta': {'ordering': "['id']", 'object_name': 'Region'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'capital_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flag_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'flag_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'weather_app.timeupdate': {
            'Meta': {'ordering': "['id']", 'object_name': 'TimeUpdate'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_tu'", 'to': u"orm['weather_app.MeteoCenter']"}),
            'time_indent': ('django.db.models.fields.TimeField', [], {}),
            'time_update': ('django.db.models.fields.TimeField', [], {})
        },
        u'weather_app.town': {
            'Meta': {'ordering': "['id']", 'object_name': 'Town'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'flag_big': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'flag_small': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'geo': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_towns'", 'to': u"orm['weather_app.Region']"}),
            'town_url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'weather_app.town_meteocenter': {
            'Meta': {'ordering': "['id']", 'object_name': 'Town_MeteoCenter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_of_town': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_date_f': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meteo_town_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_t_m'", 'to': u"orm['weather_app.MeteoCenter']"}),
            'on_main': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_meteocenters'", 'to': u"orm['weather_app.Town']"})
        },
        u'weather_app.wdata': {
            'Meta': {'ordering': "['-id']", 'object_name': 'WData'},
            'd_data_upd': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 2, 0, 0)'}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_f': ('django.db.models.fields.DateTimeField', [], {}),
            'g_hashtag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_datas_by_gh'", 'to': u"orm['weather_app.GeneralHashtag']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_datas_by_tu'", 'to': u"orm['weather_app.TimeUpdate']"}),
            'town_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_datas_by_tm'", 'to': u"orm['weather_app.Town_MeteoCenter']"})
        },
        u'weather_app.wlog': {
            'Meta': {'ordering': "['-id']", 'object_name': 'WLog'},
            'data_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_record': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 6, 2, 0, 0)'}),
            'error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meteo_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_update_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_wlogs_by_tu'", 'to': u"orm['weather_app.TimeUpdate']"}),
            'town_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_wlogs_by_tm'", 'to': u"orm['weather_app.Town_MeteoCenter']"})
        }
    }

    complete_apps = ['weather_app']