# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from lib.decorators import render_to
from models import WData, MeteoCenter, Town, Town_MeteoCenter, WLog, TimeUpdate, GeneralHashtag, Region
from datetime import datetime, timedelta

from django.template.defaultfilters import date as _date

from weather.stringparser import Parser
import re

import os
import sys
import string
import logging
import pytz

#import qsstats

from xml.etree import ElementTree
from xml.etree.ElementTree import XMLID

from weather.factory import MeteoModel

import urllib2

from forms import CitySelect, GHashtagSelect

#from qsstats import QuerySetStats, Count

from django.core.cache import cache

now = datetime.now()


@render_to('get_datas.html')
def get_datas(request):


#    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

    out = {}

    for meteocenter in MeteoCenter.objects.all():

        WModel = MeteoModel(meteocenter.name)

        for town_meteo in meteocenter.get_t_m.all():
            town = town_meteo.town

            # Логирование
            log = WLog()
            log.town_meteo_id        = town_meteo.id
            log.time_update_meteo_id = 1   #time_update  !!!!
            error                    = ''
            meteocenter_xml = str(meteocenter.xml).replace('Town', town_meteo.id_of_town)

            try:

                # Пытаемся открыть файл
                try:
                    meteo_tree = ElementTree.parse(urllib2.urlopen(meteocenter_xml))#(open(meteocenter_xml))#(urllib2.urlopen(meteocenter_xml))

                # Если файл не удалось открыть, возвращаем ошибку
    #            except IOError as e:
    #                log.error = "I/O error({0}): {1} ".format(e.errno, e.strerror) + ', ' + meteocenter_xml + ', ' + error
    #                log.save()
    #                break

                except Exception:
                    import traceback

                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                    print ''.join('!! ' + line for line in lines)  # Log it or whatever here

                    log.error = u"error: %s , %s, %s" % (Exception.message, meteocenter_xml, error) + '\n' + '\n'.join('!! ' + line for line in lines)
                    log.save()
                    break

                # Навзание города в метеоцентре
                meteo_town_name = town_meteo.meteo_town_name

                # Возвращает принятое название города
                received_town_name = WModel.get_meteo_town_name(meteo_tree)

                # Если названия не совпадаю, то запись данных не производится, а в лог возвращается принятое название города
                if received_town_name and received_town_name != town_meteo.meteo_town_name:
                    log.error = u'\n Вместо %20s    принят %20s (ссылка- %s)' % (meteo_town_name, received_town_name, meteocenter_xml)
                    log.save()
#                    break

#                if meteocenter.id == 11 :
#                    print 'meteo_town_name----------->', meteo_town_name, 'received_town_name----------->', received_town_name

                if received_town_name == town_meteo.meteo_town_name or received_town_name == False:

                    WModel_last_date_f = WModel.last_date_f(meteo_tree, meteocenter)#.replace(tzinfo=None)

#                    print '-----%-20s ----WModel_last_date_f---> %-s ----town_meteo.last_date_f--> %-s' % (town_meteo, WModel_last_date_f, town_meteo.last_date_f)

                    if WModel_last_date_f != town_meteo.last_date_f:
                        log.meteo_update = True
#                        print '------------------------------------------------------------------------------------------------WModel_last_date_f != town_meteo.last_date_f'
                        
                        # Сохраняем в БД дату последнего прогноза(pubDate - дату обновления прогноза)
                        town_meteo.last_date_f = WModel_last_date_f
                        town_meteo.save()

                        # Цикл по всем хэштегам метеоцентра(предоставляемым дынным)
                        for hashtag in meteocenter.get_gm_hashtags.all():
                            if not hashtag.s_timestep:
                                fs_array = [(f, 0) for f in meteo_tree.iter(meteocenter.f_timestep)]
                            else:
                                fs_array = [(f, s) for f in meteo_tree.iter(meteocenter.f_timestep) for s in f.iter(meteocenter.s_timestep)]

    #                        if log.meteo_update == True:
                            for f_timestep, s_timestep in fs_array:
                                add_data = WData()
                                #add_data.town_id        = town.id
                                add_data.town_meteo_id  = town_meteo.id
                                add_data.time_id        = 1 #time_update.time_update
                                add_data.g_hashtag_id   = hashtag.g_hashtag.id
                                add_data.date_f         = WModel.get_datetime(f_timestep, meteocenter, s_timestep, hashtag.g_hashtag.g_hashtag)#.replace(tzinfo=None)


                                # Хештег первого или второго уровня
                                timestep = s_timestep if hashtag.s_timestep else f_timestep
                                try:
                                    add_data.data      = WModel.get_data(timestep, hashtag)
                                except:
                                    add_data.data      = -100

                                # Если данные не ошибочные, то сохранить
                                if add_data.data and add_data.data != -100:
                                    try:
                                        add_data.save()
                                        print u'%s, %20s - %20s, %40s - %-20s' % (add_data.date_f.strftime("%d-%m-%Y %H:%M"), add_data.town_meteo.town, add_data.town_meteo.meteocenter, add_data.g_hashtag, add_data.data)
                                    except ValueError as ve:
                                        log.error  = u'\n ValueError({0}): {1}'.format(ve.errno, ve.strerror)
                                elif add_data.data == -100:
                                    error += u'\n%30s на %s - не были сохранены т.к. = -100' % (hashtag.g_hashtag.name, add_data.date_f.strftime("%d-%m-%Y %H:%M"))
                                    print u'\n%30s на %s - не были сохранены т.к. = -100' % (hashtag.g_hashtag.name, add_data.date_f.strftime("%d-%m-%Y %H:%M"))


                if log.meteo_update and error == '':
                    log.data_update = True

                if log.meteo_update and error != '': 
                    log.data_update = False
                    log.error  = u'Не все данные были успешно обновлены: %s' % error  + '\n\n' + meteocenter_xml

                if log.meteo_update == False:
                    log.error   = u'Предоставляемые данные не записаны в БД т.к. они не были обновлены\nпринятые данные:  '+WModel_last_date_f.strftime("%d-%m-%Y %H:%M")+u'\nпоследние данные: '+town_meteo.last_date_f.strftime("%d-%m-%Y %H:%M") + '\n' + meteocenter_xml
                log.save()

            except Exception as e:
                log.data_update  = False
                log.meteo_update = False

                import traceback

                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ''.join('!! ' + line for line in lines)  # Log it or whatever here

                log.error = u'\nПадение сервера: %s' % e  + '\n' + meteocenter_xml + '\n' + '\n'.join('!! ' + line for line in lines)
                log.save()

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

    if cache.get_many([town_url
            , ('preview_on_main_data_for_%s'        % town_url)
            , ('preview_on_main_town_meteos_for_%s' % town_url)
            , ('preview_towns_in_region_%s'         % town_url)
            , ('preview_temp_range_%s'              % town_url)
            , ('preview_last_temp_range_max_%s'     % town_url)
            , ('preview_last_temp_range_min_%s'     % town_url)]):

        out['town']                = cache.get(town_url)
        out['all_data_for_town']   = cache.get('preview_on_main_data_for_%s'        % town_url)
        out['town_meteos']         = cache.get('preview_on_main_town_meteos_for_%s' % town_url)
        out['towns_in_region']     = cache.get('preview_towns_in_region_%s'         % town_url)
        out['temp_range']          = cache.get('preview_temp_range_%s'              % town_url)
        out['last_temp_range_max'] = cache.get('preview_last_temp_range_max_%s'     % town_url)
        out['last_temp_range_min'] = cache.get('preview_last_temp_range_min_%s'     % town_url)

        print 1

    else:
        out['town']              = Town.objects.filter(town_url=town_url)[0]
        out['all_data_for_town'] = WData.objects.filter(town_meteo__town=out['town']).filter(town_meteo__on_main=True)
        out['town_meteos']       = out['town'].get_meteocenters.all().filter(on_main=True)
        out['towns_in_region']   = out['town'].region.get_towns.all()

        temp_range = []
        temp_range.extend([get_max_min_data_for_town(region_town) for region_town in out['towns_in_region']])

        out['temp_range']          = temp_range
        out['last_temp_range_max'] = last_range_t(out['all_data_for_town'], out['town_meteos'], "max_t")
        out['last_temp_range_min'] = last_range_t(out['all_data_for_town'], out['town_meteos'], "min_t")

        cache.set_many({town_url                        : out['town']
            , ('preview_on_main_data_for_%s'        % town_url) : out['all_data_for_town']
            , ('preview_on_main_town_meteos_for_%s' % town_url) : out['town_meteos']
            , ('preview_towns_in_region_%s'         % town_url) : out['towns_in_region']
            , ('preview_temp_range_%s'              % town_url) : out['temp_range']
            , ('preview_last_temp_range_max_%s'     % town_url) : out['last_temp_range_max']
            , ('preview_last_temp_range_min_%s'     % town_url) : out['last_temp_range_min']}
        )
        print 2

    out['now']               = now

    out['show_gr']           = True
    
    if out['show_gr']:

        if cache.get_many([('today_gr_forecasts_%s' % town_url)
                , ('3days_gr_forecasts_%s'          % town_url)
                , ('weak_gr_forecasts_%s'           % town_url)]):

            out['today_gr_forecasts'] = cache.get('today_gr_forecasts_%s' % town_url)
            out['3days_gr_forecasts'] = cache.get('3days_gr_forecasts_%s' % town_url)
            out['weak_gr_forecasts']  = cache.get('weak_gr_forecasts_%s'  % town_url)
            print 11
        else:
            out['today_gr_forecasts'] = gr_data(out['all_data_for_town'], out['town'], out['town_meteos'], 2)
            out['3days_gr_forecasts'] = gr_data(out['all_data_for_town'], out['town'], out['town_meteos'], 3)
            out['weak_gr_forecasts']  = gr_data(out['all_data_for_town'], out['town'], out['town_meteos'], 7)

            cache.set_many({('today_gr_forecasts_%s' % town_url) : out['today_gr_forecasts']
                , ('3days_gr_forecasts_%s'           % town_url) : out['3days_gr_forecasts']
                , ('weak_gr_forecasts_%s'            % town_url) : out['weak_gr_forecasts']}
            )
            print 22

    return out


def full_data_for_town(town_url):
    out = {}

    if cache.get_many([town_url
            , ('all_data_for_%s'    % town_url)
            , ('town_meteos_for_%s' % town_url)]):

        out['town']              = cache.get(town_url)
        out['all_data_for_town'] = cache.get('all_data_for_%s'    % town_url)
        out['town_meteos']       = cache.get('town_meteos_for_%s' % town_url)
#        print 1
    else:
        out['town']              = Town.objects.filter(town_url=town_url)[0]
        out['all_data_for_town'] = WData.objects.filter(town_meteo__town=out['town'])
        out['town_meteos']       = out['town'].get_meteocenters.all()

        cache.set_many({town_url                : out['town']
            , ('all_data_for_%s'    % town_url) : out['all_data_for_town']
            , ('town_meteos_for_%s' % town_url) : out['town_meteos']}
        )
#        print 2

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