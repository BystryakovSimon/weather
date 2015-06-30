# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo


class Meteo_Wunderground(AbstractMeteo):
#------------------------------------------------------ Основные функции-----------------------------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'wunderground'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        if re.search('Current Conditions', data.find(meteocenter.date_tag).text):
            return datetime.now()
        else:
            now = datetime.now()

            day_forecast = '%s' % Parser('Forecast for {:s}')(re.match(r'Forecast for \S*', data.find(meteocenter.date_tag).text).group(0))
            decimal_f = time.strptime(day_forecast,'%A')

            while now.weekday() != decimal_f.tm_wday:
                now += timedelta(days=1)

            if re.search('Night', data.find(meteocenter.date_tag).text):
                datestr = '%s-%s-%s %s:%s' % (now.year, now.month, now.day, '00', '00')
            else:
                datestr = '%s-%s-%s %s:%s' % (now.year, now.month, now.day, '12', '00')

            return datetime.strptime(datestr, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('channel'):
            out = f.find('title').text

        return Parser('{:s},  Weather from Weather Underground')(out)    

    @classmethod
    def last_date_f(cls, last_date_f_tree, meteocenter):
        out = ''
        for f in last_date_f_tree.iter('channel'):
            out = f.find('lastBuildDate').text
        return datetime.strptime(out, "%a, %d %b %Y %H:%M:%S MSK")  # Mon, 1 Oct 2012 13:00:00 MSK
#----------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-------------------------------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        if re.search('High', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'High:-?\d+',)
        else:
            return -100

    @classmethod
    def min_t(cls, data, hashtag):
        if re.search('Low', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Low:-?\d+')
        else:
            return -100

    @classmethod
    def weather_condition(cls, data, hashtag):
        try:
            if re.search('High', data.find(hashtag.m_hashtag).text):
                raise Exception
            if re.search('Low', data.find(hashtag.m_hashtag).text):
                raise Exception
        except Exception:
            return cls.parse_data(data, hashtag, r'\S* ?\S* ?\S*\.')
        else:
            return -100
#----------------------------------------------------------------------------------------------------------------------------------------------------