# -*- coding: utf-8 -*-

import sys
from xml.etree import ElementTree
from weather.factory import MeteoModel
import urllib2
from models import WData, WLog

#from celery.task import periodic_task
#from datetime import timedelta
#
#
#@periodic_task(run_every = timedelta(minutes = 1))
#
#from celery.schedules import crontab
#from celery.task import periodic_task
#
#@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon")

def meteocenter_parser(meteocenter,meteo_time_update):
    WModel = MeteoModel(meteocenter.name)

    for town_meteo in meteocenter.get_t_m.all():
        town = town_meteo.town

        # Логирование
        log = WLog()
        from datetime import datetime
        log.date_record=datetime.now()
        log.town_meteo_id        = town_meteo.id
        log.time_update_meteo_id = meteo_time_update.id   #time_update  !!!!
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
                            add_data.time_id        = meteo_time_update.id #time_update.time_update
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
#                                        add_data.data.clean_data()
                                    add_data.save()
                                    print u'%s, %20s - %20s, %40s - %-20s' % (add_data.date_f.strftime("%d-%m-%Y %H:%M"), add_data.town_meteo.town, add_data.town_meteo.meteocenter, add_data.g_hashtag, add_data.data)
                                except ValueError as ve:
                                    #log.error  = u'\n ValueError({0}): {1}'.format(ve.errno, ve.strerror)
                                    log.error  = u'Error on save\n ValueError: %s' % ve
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
