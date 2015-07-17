# -*- coding: utf-8 -*-
from django import template
import string
from datetime import datetime, timedelta
from weather.models import WData, MeteoCenter, Town, Town_MeteoCenter, WLog, TimeUpdate
from django.db.models import Q # для создания условия в фильтре
from django.core.cache import cache


register = template.Library()

now = datetime.now()

@register.filter(name='get_plus_or_minus')
def get_plus_or_minus(a):


    if not a:
        return a


    if type(a) is int:
        if 0 < a:
            return '+' + str(a)
        else:
            return '-' + str(a)

    elif a == '':
        return a
        
    elif type(a) is unicode or str:
        if 0 < int(a):
            return '+' + a
        else:
            return '-' + a





@register.filter(name='day')
def day(date, day):
    return date + timedelta(days=day)



@register.filter(name='range_t_min')
def range_t_min(town, temp_range):
    if not temp_range:
        return None
    for town_temp in temp_range:
        if town_temp[0] == town.id:
            return town_temp[1]
    return None


@register.filter(name='range_t_max')
def range_t_max(town, temp_range):
    for town_temp in temp_range:
#        print "len(town_temp) - "+ str(len(town_temp) )
        print town_temp
        if town_temp[0] == town.id:
            return town_temp[2]
    return None


@register.filter(name='from_arr')
def from_arr(from_arr, variable):
    return from_arr[variable]


@register.filter(name='current_weather')
def current_weather(town, all_data_for_town):
    # Если нет последних данных на сегодня брать последние даные на вчера
    current_weather = town.get_meteocenters.filter(meteocenter__name='current_weather')[0]
    data_for_town   = WData.objects.filter(town_meteo=current_weather).filter_by_g_hashtag('max_t')

    try:
        data = data_for_town.filter_by_day(now)[0].data
    except:
       data = '' 
    if data == '':
        try:
            data = data_for_town.filter_by_day(now - timedelta(days=1))[0].data
        except:
            data == ''

    return get_plus_or_minus(data)


@register.filter(name='get_center_map')
def get_center_map(town):
    return Town.objects.filter(id=town.region.capital_id)[0].geo


@register.filter(name='get_towns_for_region')
def get_towns_for_region(region):
    return region.get_towns.all()

#----------------------------------------------------------------------------------------------------------------------------------------
def get_data_h(town_meteo_data):
    data = {}

    try:
        max_t            = town_meteo_data.filter_by_g_hashtag('max_t').filter_by_hour()[0]
        data['max']      = max_t.data
    except:
        try:
            max_t        = town_meteo_data.filter_by_g_hashtag('max_t')[0]
            data['max']  = max_t.data
        except:
            max_t        = None
    try:
        min_t            = town_meteo_data.filter_by_g_hashtag('min_t').filter_by_hour()[0]
        data['min']      = min_t.data
    except:
        try:
            min_t        = town_meteo_data.filter_by_g_hashtag('min_t')[0]
            data['min']  = min_t.data
        except:
            min_t        = None

    if max_t != None:
        data['date_upd'] = max_t.d_data_upd.strftime("%d.%m.%y")
        data['time_upd'] = max_t.d_data_upd.strftime("%H:%M")
        data['date_f']   = max_t.date_f.strftime("%H:%M")
    elif min_t != None:
        data['date_upd'] = min_t.d_data_upd.strftime("%d.%m.%y")
        data['time_upd'] = min_t.d_data_upd.strftime("%H:%M")
        data['date_f']   = min_t.date_f.strftime("%H:%M")

    return data


def get_data(town_meteo_data):
    data = {}

    try:
        max_t            = town_meteo_data.filter_by_g_hashtag('max_t')[0]
        data['max']      = max_t.data
    except:
        max_t            = None
    try:
        min_t            = town_meteo_data.filter_by_g_hashtag('min_t')[0]
        data['min']      = min_t.data
    except:
        min_t = None

    if max_t != None:
        data['date_upd'] = max_t.d_data_upd.strftime("%d.%m.%y")
        data['time_upd'] = max_t.d_data_upd.strftime("%H:%M")
        data['date_f']   = max_t.date_f.strftime("%H:%M")
    elif min_t != None:
        data['date_upd'] = min_t.d_data_upd.strftime("%d.%m.%y")
        data['time_upd'] = min_t.d_data_upd.strftime("%H:%M")
        data['date_f']   = min_t.date_f.strftime("%H:%M")

    return data
#----------------------------------------------------------------------------------------------------------------------------------------

@register.inclusion_tag('table_data.html')
def get_data_by_tm(town_meteo, all_data_for_town):

#    if cache.get_many([('%s_data_today' % town_meteo)
#            ,('%s_data_tommorow'        % town_meteo)
#            ,('%s_data_tommorow2'       % town_meteo)]):
#
#        town_meteo_data_today     = cache.get('%s_data_today'     % town_meteo)
#        town_meteo_data_tommorow  = cache.get('%s_data_tommorow'  % town_meteo)
#        town_meteo_data_tommorow2 = cache.get('%s_data_tommorow2' % town_meteo)
#        print 1111
#    else:
    all_data_for_tm           = all_data_for_town.filter_by_t_m(town_meteo)
    town_meteo_data_today     = get_data_h(all_data_for_tm.filter_by_day(now))
    town_meteo_data_tommorow  = get_data(all_data_for_tm.filter_by_day(now + timedelta(days=1)))
    town_meteo_data_tommorow2 = get_data(all_data_for_tm.filter_by_day(now + timedelta(days=2)))

#    cache.set_many({('%s_data_today' % town_meteo): town_meteo_data_today
#        ,('%s_data_tommorow'         % town_meteo): town_meteo_data_tommorow
#        ,('%s_data_tommorow2'        % town_meteo): town_meteo_data_tommorow2})
#    print 2222
#----------------------------enfif---------

#    all_data_for_tm           = all_data_for_town.filter_by_t_m(town_meteo)
#
#    town_meteo_data_today     = get_data_h(all_data_for_tm.filter_by_day(now))
#    town_meteo_data_tommorow  = get_data(all_data_for_tm.filter_by_day(now + timedelta(days=1)))
#    town_meteo_data_tommorow2 = get_data(all_data_for_tm.filter_by_day(now + timedelta(days=2)))

    return {
        'town_meteo_data_today'      : town_meteo_data_today
        ,'town_meteo_data_tommorow'  : town_meteo_data_tommorow
        ,'town_meteo_data_tommorow2' : town_meteo_data_tommorow2
    }

@register.inclusion_tag('main_table_data.html')
def get_main_data_by_tm(town_meteo, all_data_for_town):
#    all_data_for_tm           = all_data_for_town.filter_by_t_m(town_meteo)

#    town_meteo_data_today     = get_data_h(all_data_for_tm.filter_by_day(now))

#    if cache.get_many([('%s_data_today' % town_meteo)]):
#        town_meteo_data_today = cache.get('%s_data_today' % town_meteo)
#        print 111
#    else:
    all_data_for_tm       = all_data_for_town.filter_by_t_m(town_meteo)
    town_meteo_data_today = get_data_h(all_data_for_tm.filter_by_day(now))

    cache.set_many({('%s_data_today' % town_meteo): town_meteo_data_today})
#    print 222
#----------------------------enfif---------

    return {
        'town_meteo_data_today' : town_meteo_data_today
        ,'meteocenter_link'     : town_meteo.meteocenter.link
        ,'meteocenter_flag'     : town_meteo.meteocenter.flag
    }
#----------------------------------------------------------------------------------------------------------------------------------------

def get_town_full7_data(town_meteo_data):
    data = {}
    max_temp = -100
    min_temp =  100

    try:
        data['max'] = town_meteo_data.filter_by_g_hashtag('max_t')

        for temp in data['max']:
            print 'min----', temp.date_f.strftime("%d.%m"), '------>', temp.town_meteo.meteocenter, '------', temp.data, '-----', max_temp
            if max_temp < int(temp.data):
                max_t    = temp
                max_temp = int(temp.data)
        
        data['max'] = max_t.data
    except:
        max_t            = None

    try:
        data['min'] = town_meteo_data.filter_by_g_hashtag('min_t')

        for temp in data['min']:
            print 'min----', temp.date_f.strftime("%d.%m"), '------>', temp.town_meteo.meteocenter, '------', temp.data, '-----', min_temp
            if min_temp > int(temp.data):
                min_t    = temp
                min_temp = int(temp.data)
        
        data['min'] = min_t.data
    except:
        min_t = None

    if max_t != None:
        data['date_upd'] = max_t.d_data_upd.strftime("%d.%m.%y")
        data['time_upd'] = max_t.d_data_upd.strftime("%H:%M")
        data['date_f']   = max_t.date_f.strftime("%H:%M")
    elif min_t != None:
        data['date_upd'] = min_t.d_data_upd.strftime("%d.%m.%y")
        data['time_upd'] = min_t.d_data_upd.strftime("%H:%M")
        data['date_f']   = min_t.date_f.strftime("%H:%M")

    return data



@register.inclusion_tag('table_data_full7.html')
def get_town_full7(town_meteo, all_data_for_town):

#    if cache.get_many([('%s_data_full7_day1' % town_meteo)
#            ,('%s_data_full7_day2'           % town_meteo)
#            ,('%s_data_full7_day3'           % town_meteo)
#            ,('%s_data_full7_day4'           % town_meteo)
#            ,('%s_data_full7_day5'           % town_meteo)
#            ,('%s_data_full7_day6'           % town_meteo)
#            ,('%s_data_full7_day7'           % town_meteo)]):
#
#        town_meteo_data_day1 = cache.get('%s_data_full7_day1' % town_meteo)
#        town_meteo_data_day2 = cache.get('%s_data_full7_day2' % town_meteo)
#        town_meteo_data_day3 = cache.get('%s_data_full7_day3' % town_meteo)
#        town_meteo_data_day4 = cache.get('%s_data_full7_day4' % town_meteo)
#        town_meteo_data_day5 = cache.get('%s_data_full7_day5' % town_meteo)
#        town_meteo_data_day6 = cache.get('%s_data_full7_day6' % town_meteo)
#        town_meteo_data_day7 = cache.get('%s_data_full7_day7' % town_meteo)
#        print 1111
#    else:
    all_data_for_tm      = all_data_for_town.filter_by_t_m(town_meteo)
    town_meteo_data_day1 = get_town_full7_data(all_data_for_tm.filter_by_day(now))
    town_meteo_data_day2 = get_town_full7_data(all_data_for_tm.filter_by_day(now + timedelta(days=1)))
    town_meteo_data_day3 = get_town_full7_data(all_data_for_tm.filter_by_day(now + timedelta(days=2)))
    town_meteo_data_day4 = get_town_full7_data(all_data_for_tm.filter_by_day(now + timedelta(days=3)))
    town_meteo_data_day5 = get_town_full7_data(all_data_for_tm.filter_by_day(now + timedelta(days=4)))
    town_meteo_data_day6 = get_town_full7_data(all_data_for_tm.filter_by_day(now + timedelta(days=5)))
    town_meteo_data_day7 = get_town_full7_data(all_data_for_tm.filter_by_day(now + timedelta(days=6)))

#    cache.set_many({('%s_data_full7_day1' % town_meteo): town_meteo_data_day1
#        ,('%s_data_full7_day2' % town_meteo): town_meteo_data_day2
#        ,('%s_data_full7_day3' % town_meteo): town_meteo_data_day3
#        ,('%s_data_full7_day4' % town_meteo): town_meteo_data_day4
#        ,('%s_data_full7_day5' % town_meteo): town_meteo_data_day5
#        ,('%s_data_full7_day6' % town_meteo): town_meteo_data_day6
#        ,('%s_data_full7_day7' % town_meteo): town_meteo_data_day7})
#    print 2222
#----------------------------enfif---------

#    all_data_for_tm           = all_data_for_town.filter_by_t_m(town_meteo)
#
#    town_meteo_data_today     = get_data_h(all_data_for_tm.filter_by_day(now))
#    town_meteo_data_tommorow  = get_data(all_data_for_tm.filter_by_day(now + timedelta(days=1)))
#    town_meteo_data_tommorow2 = get_data(all_data_for_tm.filter_by_day(now + timedelta(days=2)))

    return {
        'town_meteo_data_day1'  : town_meteo_data_day1
        ,'town_meteo_data_day2' : town_meteo_data_day2
        ,'town_meteo_data_day3' : town_meteo_data_day3
        ,'town_meteo_data_day4' : town_meteo_data_day4
        ,'town_meteo_data_day5' : town_meteo_data_day5
        ,'town_meteo_data_day6' : town_meteo_data_day6
        ,'town_meteo_data_day7' : town_meteo_data_day7
    }


#----------------------------------------------------------------------------------------------------------------------------------------


def get_town_full3_data(town_meteo_data, date):
    data = {}

    town_meteo_data_max  = town_meteo_data.filter_by_g_hashtag('max_t')
    town_meteo_data_min  = town_meteo_data.filter_by_g_hashtag('min_t')

    try:
        data['max_4_10'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 4)
            , date.replace(date.year, date.month, date.day, 10)
        )

        data['max_10_16'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 10)
            , date.replace(date.year, date.month, date.day, 16)
        )

        data['max_16_22'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 16)
            , date.replace(date.year, date.month, date.day, 22)
        )

        data['max_22_4'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 22)
            , date.replace(date.year, date.month, (date+timedelta(days=1)).day, 4)
        )
    except:
        max_t = None

    try:
        data['min_4_10'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 4)
            , date.replace(date.year, date.month, date.day, 10)
        )

        data['min_10_16'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 10)
            , date.replace(date.year, date.month, date.day, 16)
        )

        data['min_16_22'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 16)
            , date.replace(date.year, date.month, date.day, 22)
        )

        data['min_22_4'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 22)
            , date.replace(date.year, date.month, (date+timedelta(days=1)).day, 4)
        )
    except:
        min_t = None

    return data





@register.inclusion_tag('table_data_full3.html')
def get_town_full3(town_meteo, all_data_for_town):

#    if cache.get_many([('%s_data_full3_day1' % town_meteo)
#            ,('%s_data_full3_day2'           % town_meteo)
#            ,('%s_data_full3_day3'           % town_meteo)]):
#
#        town_meteo_data_day1 = cache.get('%s_data_full3_day1' % town_meteo)
#        town_meteo_data_day2 = cache.get('%s_data_full3_day2' % town_meteo)
#        town_meteo_data_day3 = cache.get('%s_data_full3_day3' % town_meteo)
#    else:
    all_data_for_tm      = all_data_for_town.filter_by_t_m(town_meteo)
    town_meteo_data_day1 = get_town_full3_data(all_data_for_tm, now)
    town_meteo_data_day2 = get_town_full3_data(all_data_for_tm, now + timedelta(days=1))
    town_meteo_data_day3 = get_town_full3_data(all_data_for_tm, now + timedelta(days=2))

#    cache.set_many({('%s_data_full3_day1' % town_meteo): town_meteo_data_day1
#        ,('%s_data_full3_day2' % town_meteo): town_meteo_data_day2
#        ,('%s_data_full3_day3' % town_meteo): town_meteo_data_day3})
#----------------------------enfif---------

    print 'town_meteo_data_day1 ', town_meteo_data_day1
    return {
        'town_meteo_data_day1'  : town_meteo_data_day1
        ,'town_meteo_data_day2' : town_meteo_data_day2
        ,'town_meteo_data_day3' : town_meteo_data_day3
    }

def get_town_full_data(town_meteo_data, date):
    data = {}
    town_meteo_data_max  = town_meteo_data.filter_by_g_hashtag('max_t')
    town_meteo_data_min  = town_meteo_data.filter_by_g_hashtag('min_t')

    try:
        data['max_0'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 0)
            , date.replace(date.year, date.month, date.day, 1)
        )
        data['max_1'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 1)
            , date.replace(date.year, date.month, date.day, 2)
        )
        data['max_2'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 2)
            , date.replace(date.year, date.month, date.day, 3)
        )
        data['max_3'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 3)
            , date.replace(date.year, date.month, date.day, 4)
        )
        data['max_4'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 4)
            , date.replace(date.year, date.month, date.day, 5)
        )
        data['max_5'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 5)
            , date.replace(date.year, date.month, date.day, 6)
        )
        data['max_6'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 6)
            , date.replace(date.year, date.month, date.day, 7)
        )
        data['max_7'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 7)
            , date.replace(date.year, date.month, date.day, 8)
        )
        data['max_8'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 8)
            , date.replace(date.year, date.month, date.day, 9)
        )
        data['max_9'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 9)
            , date.replace(date.year, date.month, date.day, 10)
        )
        data['max_10'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 10)
            , date.replace(date.year, date.month, date.day, 11)
        )
        data['max_11'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 11)
            , date.replace(date.year, date.month, date.day, 12)
        )
        data['max_12'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 12)
            , date.replace(date.year, date.month, date.day, 13)
        )
        data['max_13'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 13)
            , date.replace(date.year, date.month, date.day, 14)
        )
        data['max_14'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 14)
            , date.replace(date.year, date.month, date.day, 15)
        )
        data['max_15'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 15)
            , date.replace(date.year, date.month, date.day, 16)
        )
        data['max_16'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 16)
            , date.replace(date.year, date.month, date.day, 17)
        )
        data['max_17'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 17)
            , date.replace(date.year, date.month, date.day, 18)
        )
        data['max_18'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 18)
            , date.replace(date.year, date.month, date.day, 19)
        )
        data['max_19'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 19)
            , date.replace(date.year, date.month, date.day, 20)
        )
        data['max_20'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 20)
            , date.replace(date.year, date.month, date.day, 21)
        )
        data['max_21'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 21)
            , date.replace(date.year, date.month, date.day, 22)
        )
        data['max_22'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 22)
            , date.replace(date.year, date.month, date.day, 23)
        )
        data['max_23'] = town_meteo_data_max.filter_by_time(
            date.replace(date.year, date.month, date.day, 23)
            , date.replace(date.year, date.month, (date+timedelta(days=1)).day, 0)
        )

    except:
        max_t = None

    try:

        data['min_0'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 0)
            , date.replace(date.year, date.month, date.day, 1)
        )
        data['min_1'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 1)
            , date.replace(date.year, date.month, date.day, 2)
        )
        data['min_2'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 2)
            , date.replace(date.year, date.month, date.day, 3)
        )
        data['min_3'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 3)
            , date.replace(date.year, date.month, date.day, 4)
        )
        data['min_4'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 4)
            , date.replace(date.year, date.month, date.day, 5)
        )
        data['min_5'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 5)
            , date.replace(date.year, date.month, date.day, 6)
        )
        data['min_6'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 6)
            , date.replace(date.year, date.month, date.day, 7)
        )
        data['min_7'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 7)
            , date.replace(date.year, date.month, date.day, 8)
        )
        data['min_8'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 8)
            , date.replace(date.year, date.month, date.day, 9)
        )
        data['min_9'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 9)
            , date.replace(date.year, date.month, date.day, 10)
        )
        data['min_10'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 10)
            , date.replace(date.year, date.month, date.day, 11)
        )
        data['min_11'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 11)
            , date.replace(date.year, date.month, date.day, 12)
        )
        data['min_12'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 12)
            , date.replace(date.year, date.month, date.day, 13)
        )
        data['min_13'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 13)
            , date.replace(date.year, date.month, date.day, 14)
        )
        data['min_14'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 14)
            , date.replace(date.year, date.month, date.day, 15)
        )
        data['min_15'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 15)
            , date.replace(date.year, date.month, date.day, 16)
        )
        data['min_16'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 16)
            , date.replace(date.year, date.month, date.day, 17)
        )
        data['min_17'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 17)
            , date.replace(date.year, date.month, date.day, 18)
        )
        data['min_18'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 18)
            , date.replace(date.year, date.month, date.day, 19)
        )
        data['min_19'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 19)
            , date.replace(date.year, date.month, date.day, 20)
        )
        data['min_20'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 20)
            , date.replace(date.year, date.month, date.day, 21)
        )
        data['min_21'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 21)
            , date.replace(date.year, date.month, date.day, 22)
        )
        data['min_22'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 22)
            , date.replace(date.year, date.month, date.day, 23)
        )
        data['min_23'] = town_meteo_data_min.filter_by_time(
            date.replace(date.year, date.month, date.day, 23)
            , date.replace(date.year, date.month, (date+timedelta(days=1)).day, 0)
        )
    except:
        min_t = None

    return data


@register.inclusion_tag('table_data_full.html')
def get_town_full(town_meteo, all_data_for_town):

    if cache.get_many([('%s_data_full_day1' % town_meteo)]):
        town_meteo_data_day1 = cache.get('%s_data_full_day1' % town_meteo)
    else:
        all_data_for_tm      = all_data_for_town.filter_by_t_m(town_meteo)
        town_meteo_data_day1 = get_town_full_data(all_data_for_tm, now)

        cache.set_many({('%s_data_full_day1' % town_meteo): town_meteo_data_day1})

    print 'town_meteo_data_day1 ', town_meteo_data_day1
    return {
        'town_meteo_data_day1'  : town_meteo_data_day1
        ,'town_meteo'           : town_meteo
    }