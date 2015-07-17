# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from lib.decorators import render_to
from models import WData, MeteoCenter, Town, WLog, Region
from datetime import datetime, timedelta

#from django.template.defaultfilters import date as _date

#from weather.stringparser import Parser
#import re

#import os
#import sys
#import string
#import logging
#import pytz

#import qsstats

#from xml.etree import ElementTree
#from xml.etree.ElementTree import XMLID

#from weather.factory import MeteoModel

#import urllib2

#from forms import CitySelect, GHashtagSelect

#from qsstats import QuerySetStats, Count

#from django.core.cache import cache

now = datetime.now()


@render_to('get_datas.html')
def get_datas(request):

    from weather.wparser import meteocenter_parser

    out = {}

    for meteocenter in MeteoCenter.objects.all():

        for time_update in meteocenter.get_tu.all():
            a = now-timedelta(minutes=30)
            b = now+timedelta(minutes=30)
            if time_update.time_update>a.time() and time_update.time_update<b.time():
                meteo_time_update = time_update

                meteocenter_parser(meteocenter,meteo_time_update)

    return out


@render_to('town_preview.html')
def town_preview(request, town_url):

    from weather.graphic import gr_data
    out = {}

    def get_max_min_data_for_town(region_town):
        current_data_for_town = WData.objects.filter(town_meteo__town=region_town).filter(town_meteo__on_main=True).filter_by_day(now)
        max_min_data = []
        max_min_data.append(region_town.id)

#        try:
#            min_temp = 100
#            all_min_temp = current_data_for_town.filter_by_g_hashtag('min_t')
#
#            for temp in all_min_temp:
#                    if min_temp > int(temp.data):
#                        min_temp = int(temp.data)
#            max_min_data.append(min_temp)
            
        all_min_temp = current_data_for_town.filter_by_g_hashtag('min_t')
        min_temp = min([int(e.data) for e in all_min_temp]) if all_min_temp else []

        max_min_data.append(min_temp)
#        except Exception:
#            print u'%s' % region_town + " - min found error"

#        try:
#            max_temp = -100
#            all_max_temp = current_data_for_town.filter_by_g_hashtag('max_t')

#            for temp in all_max_temp:
#                if max_temp < int(temp.data):
#                    max_temp = int(temp.data)
                    
#            max_min_data.append(max_temp)

        all_max_temp = current_data_for_town.filter_by_g_hashtag('max_t')
        max_temp = max([int(e.data) for e in all_max_temp]) if all_max_temp else []

        max_min_data.append(max_temp)

#        except Exception:
#            print u'%s' % region_town

        return max_min_data

    def last_range_t(all_data_for_town, town_meteos, min_max):
        all_temp = []
        out      = 1000
        for tm in town_meteos:
            try:
                all_temp.append(int(all_data_for_town.get_lastest_data(tm, now, min_max)[0].data))
            except:
                qwerty = ''

        max_temp = -100
        min_temp =  100

        for temp in all_temp:

            if min_max == 'max_t':
                if max_temp < temp:
                    max_temp = temp
                out = max_temp

            elif min_max == 'min_t':
                if min_temp > temp:
                    min_temp = temp
                out = min_temp

        return out

#    if cache.get_many([town_url
#            , ('preview_on_main_data_for_%s'        % town_url)
#            , ('preview_on_main_town_meteos_for_%s' % town_url)
#            , ('preview_towns_in_region_%s'         % town_url)
#            , ('preview_temp_range_%s'              % town_url)
#            , ('preview_last_temp_range_max_%s'     % town_url)
#            , ('preview_last_temp_range_min_%s'     % town_url)]):
#
#        out['town']                = cache.get(town_url)
#        out['all_data_for_town']   = cache.get('preview_on_main_data_for_%s'        % town_url)
#        out['town_meteos']         = cache.get('preview_on_main_town_meteos_for_%s' % town_url)
#        out['towns_in_region']     = cache.get('preview_towns_in_region_%s'         % town_url)
#        out['temp_range']          = cache.get('preview_temp_range_%s'              % town_url)
#        out['last_temp_range_max'] = cache.get('preview_last_temp_range_max_%s'     % town_url)
#        out['last_temp_range_min'] = cache.get('preview_last_temp_range_min_%s'     % town_url)
#
#        print 1
#
#    else:
    
#    out['town']              = Town.objects.filter(town_url=town_url)[0]
    out['town']              = get_object_or_404(Town, town_url=town_url)
    
    out['all_data_for_town'] = WData.objects.filter(town_meteo__town=out['town']).filter(town_meteo__on_main=True)
    out['town_meteos']       = out['town'].get_meteocenters.all().filter(on_main=True)
    out['towns_in_region']   = out['town'].region.get_towns.all()

    temp_range = []
    temp_range.extend([get_max_min_data_for_town(region_town) for region_town in out['towns_in_region']])

    out['temp_range']          = temp_range
    out['last_temp_range_max'] = last_range_t(out['all_data_for_town'], out['town_meteos'], "max_t")
    out['last_temp_range_min'] = last_range_t(out['all_data_for_town'], out['town_meteos'], "min_t")

#    cache.set_many({town_url                        : out['town']
#        , ('preview_on_main_data_for_%s'        % town_url) : out['all_data_for_town']
#        , ('preview_on_main_town_meteos_for_%s' % town_url) : out['town_meteos']
#        , ('preview_towns_in_region_%s'         % town_url) : out['towns_in_region']
#        , ('preview_temp_range_%s'              % town_url) : out['temp_range']
#        , ('preview_last_temp_range_max_%s'     % town_url) : out['last_temp_range_max']
#        , ('preview_last_temp_range_min_%s'     % town_url) : out['last_temp_range_min']}
#    )
#    print 2
#----------------------------enfif---------

    out['now']               = now

    out['show_gr']           = False
    
    if out['show_gr']:

#        if cache.get_many([('today_gr_forecasts_%s' % town_url)
#                , ('3days_gr_forecasts_%s'          % town_url)
#                , ('weak_gr_forecasts_%s'           % town_url)]):
#
#            out['today_gr_forecasts'] = cache.get('today_gr_forecasts_%s' % town_url)
#            out['3days_gr_forecasts'] = cache.get('3days_gr_forecasts_%s' % town_url)
#            out['weak_gr_forecasts']  = cache.get('weak_gr_forecasts_%s'  % town_url)
#            print 11
#        else:
        out['today_gr_forecasts'] = gr_data(out['all_data_for_town'], out['town'], out['town_meteos'], 2)
        out['3days_gr_forecasts'] = gr_data(out['all_data_for_town'], out['town'], out['town_meteos'], 3)
        out['weak_gr_forecasts']  = gr_data(out['all_data_for_town'], out['town'], out['town_meteos'], 7)

#        cache.set_many({('today_gr_forecasts_%s' % town_url) : out['today_gr_forecasts']
#            , ('3days_gr_forecasts_%s'           % town_url) : out['3days_gr_forecasts']
#            , ('weak_gr_forecasts_%s'            % town_url) : out['weak_gr_forecasts']}
#        )
#        print 22

    return out


def full_data_for_town(town_url):
    out = {}

#    if cache.get_many([town_url
#            , ('all_data_for_%s'    % town_url)
#            , ('town_meteos_for_%s' % town_url)]):
#
#        out['town']              = cache.get(town_url)
#        out['all_data_for_town'] = cache.get('all_data_for_%s'    % town_url)
#        out['town_meteos']       = cache.get('town_meteos_for_%s' % town_url)
##        print 1
#    else:
    out['town']              = Town.objects.filter(town_url=town_url)[0]
    out['all_data_for_town'] = WData.objects.filter(town_meteo__town=out['town'])
    out['town_meteos']       = out['town'].get_meteocenters.all()

#    cache.set_many({town_url                : out['town']
#        , ('all_data_for_%s'    % town_url) : out['all_data_for_town']
#        , ('town_meteos_for_%s' % town_url) : out['town_meteos']}
#    )
#        print 2
#----------------------------enfif---------
    out['now']               = now

    return out


@render_to('town_full.html')
def town_full(request, town_url):
    return full_data_for_town(town_url)


@render_to('town_full3.html')
def town_full3(request, town_url):
    return full_data_for_town(town_url)


@render_to('town_full7.html')
def town_full7(request, town_url):
    return full_data_for_town(town_url)


@render_to('main.html')
def main(request):
    out = {}

    out['all_regions'] = Region.objects.all()

    return out




#@render_to('meteocenter_full.html')
#def meteocenter_full(request, town_url, meteocenter_name):
#    out = {}
#
#
#    if cache.get_many([town_url
#            , ('all_data_for_%s'    % town_url)
#            , ('town_meteos_for_%s' % town_url)]):
#
#        out['town']              = cache.get(town_url)
#        out['all_data_for_town'] = cache.get('all_data_for_%s' % town_url)
#        out['town_meteos']       = cache.get('town_meteos_for_%s' % town_url)
##        print 1
#    else:
#        out['meteocenter']               = MeteoCenter.objects.filter(name=meteocenter_name)[0]
#        out['town']                      = Town.objects.filter(town_url=town_url)[0]
#
#        out['providedatas']              = out['meteocenter'].get_gm_hashtags.all()
#
#        out['meteocenter_data_for_town'] = WData.objects.filter(town_meteo__meteocenter=out['meteocenter'])
#
#        cache.set_many({town_url                : out['town']
#            , ('all_data_for_%s'    % town_url) : out['all_data_for_town']
#            , ('town_meteos_for_%s' % town_url) : out['town_meteos']}
#        )
##        print 2
#
#    out['now']               = now
#
#    return out