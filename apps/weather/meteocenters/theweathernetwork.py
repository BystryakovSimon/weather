# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_TheWeatherNetWork(AbstractMeteo):
#------------------------------------------------------ Основные функции---------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'theweathernetwork'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        if re.search('Current Weather', data.find(meteocenter.date_tag).text):
            return datetime.now()
        else:
#            print data.find(meteocenter.date_tag).text
#            return datetime.strptime(data.find(meteocenter.date_tag).text, ("%A, %B %d, %Y %s:%s" % (('12' if hashtag == 'max_t' else '00'), '00')))
#
#            datestr = '%s-%s-%s %s:%s' % (now.year, now.month, now.day, ('12' if hashtag == 'max_t' else '00'), '00')
#            return datetime.strptime(datestr, meteocenter.date_reg)
#
#
#            print data.find(meteocenter.date_tag).text
            out = datetime.strptime(data.find(meteocenter.date_tag).text, "%A, %B %d, %Y")
            return out+timedelta(hours=12) if hashtag == 'max_t' else out


    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('channel'):
            out = f.find('title').text

        return Parser('The Weather Network - {:s}, Russia')(out)

    @classmethod
    def last_date_f(cls, last_date_f_tree, meteocenter):
        out = ''
        for f in last_date_f_tree.iter('item'): 
            if out == '':
                out = f.find('pubDate').text
#                return datetime.strptime(out, "%a, %d %b %Y %H:%M:%S \d+")  # Mon, 05 Nov 2012, 12:00:00 RST
                return datetime.strptime(re.search('\S*, \d+ \S* \d+ \d+:\d+:\d+', out).group(), "%a, %d %b %Y %H:%M:%S")  # Mon, 05 Nov 2012, 12:00:00 RST

#re.search('\S* ', out).group()
#Parser('\S* ')(out)

#        return datetime.strptime(out, "%a, %d %B, %Y, %H:%M:%S RST")
#--------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-----------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        if re.search('High', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'High\s*-?\d+')
        else:
            return -100

    @classmethod
    def min_t(cls, data, hashtag):
        if re.search('Low', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Low\s*-?\d+',)
        else:
            return -100

    @classmethod
    def pop(cls, data, hashtag):
        if re.search('P.O.P.', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'P.O.P.\s*\d+',)
        else:
            return -100

    @classmethod
    def humidity_max(cls, data, hashtag):
        if re.search('Humidity', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Humidity\s*\d+',)
        else:
            return -100

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        try:
            if re.search('Wind', data.find(hashtag.m_hashtag).text):
                return cls.parse_data(data, hashtag, r'Wind\s*\S*\s*\d?',)
        except:
#        else:
            return -100

    @classmethod
    def wind_dir(cls, data, hashtag):
        if re.search('Wind', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Wind\s*\S*-?\S*',)
        else:
            return -100
#--------------------------------------------------------------------------------------------------------------------------------