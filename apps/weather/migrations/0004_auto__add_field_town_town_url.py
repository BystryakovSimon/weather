# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Town.town_url'
        db.add_column('weather_town', 'town_url',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Town.town_url'
        db.delete_column('weather_town', 'town_url')


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
            'showing_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_towns'", 'to': "orm['weather.Region']"}),
            'town_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'weather.town_meteocenter': {
            'Meta': {'ordering': "['id']", 'object_name': 'Town_MeteoCenter'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_of_town': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_date_f': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meteo_town_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meteocenter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_t_m'", 'to': "orm['weather.MeteoCenter']"}),
            'on_main': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_meteocenters'", 'to': "orm['weather.Town']"})
        },
        'weather.wdata': {
            'Meta': {'ordering': "['-id']", 'object_name': 'WData'},
            'd_data_upd': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 29, 0, 0)'}),
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
            'date_record': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 29, 0, 0)'}),
            'error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meteo_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_update_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_wlogs_by_tu'", 'to': "orm['weather.TimeUpdate']"}),
            'town_meteo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'get_wlogs_by_tm'", 'to': "orm['weather.Town_MeteoCenter']"})
        }
    }

    complete_apps = ['weather']