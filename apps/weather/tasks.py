# -*- coding: utf-8 -*-
#from datetime import timedelta, datetime
#
#from django.shortcuts import get_object_or_404,redirect
#from lib.decorators import render_to
#from models import WData, MeteoCenter, Town, TimeUpdate, Town_MeteoCenter, WLog
#import time
#
#from weather.stringparser import Parser
#import re
#
#import os
#import sys
#import string
#import pytz
#
#from xml.etree import ElementTree
#from xml.etree.ElementTree import XMLID
#
#from weather.factory import MeteoModel
#
#from celery.schedules import crontab
#from celery.task import periodic_task
#
#import urllib2

from django.shortcuts import get_object_or_404, redirect
from lib.decorators import render_to
from models import WData, MeteoCenter, Town, WLog, Region
from datetime import datetime, timedelta
#from celery import shared_task

from celery import task


@task(name='weather.tasks.WParser')
#@app.task(name='settings.task.WParser')
#@periodic_task(run_every=crontab(minute=1,))
#@shared_task
def WParser():
    from weather.wparser import meteocenter_parser

    out = {}

    for meteocenter in MeteoCenter.objects.all():

        for time_update in meteocenter.get_tu.all():
            a = datetime.now()#-timedelta(minutes=30)
            #b = datetime.now()+timedelta(minutes=30)
            b = datetime.now()+timedelta(hours=1)
            if time_update.time_update>a.time() and time_update.time_update<b.time():
                meteo_time_update = time_update

                meteocenter_parser(meteocenter,meteo_time_update)



#
#@periodic_task(run_every=crontab(minute=5,))
#def WParcer():
#    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
#
#    hour_ago    = datetime.now() - timedelta(hours=1) # час назад 
#    now         = datetime.now()                      # текущее время
#
#    for time_update in TimeUpdate.objects.all():
#        print '2'
#        if hour_ago.strftime("%H:%M") < time_update.time_update.strftime("%H:%M") < now.strftime("%H:%M"):    # за прошедший час
            #
#            meteocenter = time_update.meteocenter
            #
#            WModel = MeteoModel(meteocenter.name)
                    #
#            for town_meteo in meteocenter.get_t_m.all():
#                town = town_meteo.town
#
#                # Логирование
#                log = WLog()
#                log.town_meteo_id        = town_meteo.id
#                log.time_update_meteo_id = time_update.id
#                error = ''
#
#                meteocenter_xml = str(meteocenter.xml).replace('Town', town_meteo.id_of_town)
#
#                # Пытаемся открыть файл
#                try:
#                    meteo_tree = ElementTree.parse(urllib2.urlopen(meteocenter_xml))
#
#                # Если файл не удалось открыть, возвращаем ошибку
#                except IOError as e:
#                    log.error = "I/O error({0}): {1} ".format(e.errno, e.strerror) + ', ' + meteocenter_xml + ', ' + error
#                    log.save()
#                    break
#
#                # Навзание города в метеоцентре
#                meteo_town_name = town_meteo.meteo_town_name
#
#                # Возвращает принятое название города
#                received_town_name = WModel.get_meteo_town_name(meteo_tree)
#                if received_town_name == False:
#                    received_town_name = meteo_town_name
#
#                # Если названия не совпадаю, то запись данных не производится, а в лог возвращается принятое название города
#                elif received_town_name != meteo_town_name and received_town_name != False:
#                    log.error = u'\n Вместо %20s    принят %20s (ссылка- %s)' % (meteo_town_name, received_town_name, meteocenter_xml)
#                    log.save()
#
#                if received_town_name == meteo_town_name:
#
#                    # Цикл по всем хэштегам метеоцентра(предоставляемым дынным)
#                    for hashtag in meteocenter.get_gm_hashtags.all():
#                        if not hashtag.s_timestep:
#                            fs_array = [(f, 0) for f in meteo_tree.iter(meteocenter.f_timestep)]
#                        else:
#                            fs_array = [(f, s) for f in meteo_tree.iter(meteocenter.f_timestep) for s in f.iter(meteocenter.s_timestep)]
#
#                        # Берем последнюю дату прогноза(pubDate - дату обновления прогноза)
#                        WModel_last_date_f = WModel.last_date_f(meteo_tree, meteocenter, fs_array)
                        #
#                        if WModel_last_date_f.replace(tzinfo=pytz.UTC) != town_meteo.last_date_f:
#                            log.meteo_update = True
#                        if log.meteo_update == True:
#                            for f_timestep, s_timestep in fs_array:
#                                add_data = WData()
#                                add_data.town_meteo_id        = town_meteo.id
#                                #add_data.meteocenter_id = meteocenter.id
#                                add_data.time_id        = time_update.id
#                                add_data.g_hashtag_id   = hashtag.g_hashtag.id
#                                add_data.date_f         = WModel.get_datetime(f_timestep, meteocenter, s_timestep)
#
#                                # Хештег первого или второго уровня
#                                timestep = s_timestep if hashtag.s_timestep else f_timestep
#                                try:
#                                    add_data.data      = WModel.get_data(timestep, hashtag)
#                                except:
#                                    add_data.data      = -100
                                    #
#                                # Если данные не ошибочные, то сохранить
#                                if add_data.data and add_data.data != -100:
#                                    try:
#                                        add_data.save()
#                                        print u' %20s - %20s, %40s - %-20s' % (add_data.town_meteo.town, add_data.town_meteo.meteocenter, add_data.g_hashtag, add_data.data)
#                                    except ValueError as ve:
#                                        log.error  = '\n ValueError({0}): {1}'.format(ve.errno, ve.strerror)
#                                elif add_data.data == -100:
#                                    error += u'\n%30s на %s - не были сохранены т.к. = -100' % (hashtag.g_hashtag.name, add_data.date_f.strftime("%d-%m-%Y %H:%M"))
                    #
#                        # Сохраняем в БД дату последнего прогноза(pubDate - дату обновления прогноза)
#                        town_meteo.last_date_f = WModel_last_date_f.replace(tzinfo=pytz.UTC)
#                        town_meteo.save()
#
#                        if log.meteo_update == True and error == '':
#                                log.data_update = True
#
#                        if log.meteo_update == True and error != '': 
#                            log.data_update = False
#                            log.error  = u'Не все данные были успешно обновлены: %s' % error
#
#                        if log.meteo_update == False:
#                            log.error   = 'Предоставляемые данные не записаны в БД т.к. они не были обновлены'
#                        log.save()