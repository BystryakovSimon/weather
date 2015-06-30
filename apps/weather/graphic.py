# -*- coding: utf-8 -*-

from django.template.defaultfilters import date as _date
from datetime import datetime, timedelta
now = datetime.now()

# Здесь формирауются данные для графика [['дата', rp5, gis], ['дата', rp5, gis]]
def gr_data(all_data_for_town, town, town_meteos, days):
    data      = []
    gr_shapka = []

    def get_meteos_data(data_for_town_by_t_m, time_from, time_to):
        avg      = 0
        max_data = data_for_town_by_t_m.filter_by_g_hashtag('max_t').filter_by_range_of_time(time_from, time_to)
        min_data = data_for_town_by_t_m.filter_by_g_hashtag('min_t').filter_by_range_of_time(time_from, time_to)

        if max_data == None and min_data == None:
            return avg
        else:
            if (min_data != None) and (max_data != None):
                return (int(max_data) + int(min_data)) / 2
            elif min_data == None:
                return int(max_data)
            elif max_data == None:
                return int(min_data)

        return avg


    for a in range(days):  
        date = now + timedelta(days=a)

        hours = [4,10,16,22]

        if a == 0:
            # на сегодня для оставшихся часов в день
            for h in hours:
                date_hour = datetime.strptime(
                    '%s-%s-%s %s:%s' % (date.year, date.month, date.day, h, '00')
                    , "%Y-%m-%d %H:%M"
                )

                if h > now.hour:
                    data.append(u'[\'%s\',%s]' % (
                        _date(date_hour, "d D H:00")
                        , ', '.join([
                            '%s' % get_meteos_data(all_data_for_town.filter_by_t_m(t_m), date_hour - timedelta(hours=6), date_hour)
                            for t_m in  town_meteos
                        ])
                    ))
        else:
            # На остальные дни
            for h in hours:
                date_hour = datetime.strptime(
                    '%s-%s-%s %s:%s' % (date.year, date.month, date.day, h, '00')
                    , "%Y-%m-%d %H:%M"
                )
                data.append(u'[\'%s\',%s]' % (
                    _date(date_hour, "d D H:00")
                    , ', '.join(['%s' % get_meteos_data(all_data_for_town.filter_by_t_m(t_m), date_hour - timedelta(hours=6), date_hour) 
                        for t_m in  town_meteos])
                    )
                )

    gr_shapka = u'[\'Day\', %s]' % (', '.join([
        "'%s'" % meteos.meteocenter.showing_name 
        for meteos in  town_meteos
    ]))

    return {
        'data'        : data
        , 'gr_shapka' : gr_shapka
    }