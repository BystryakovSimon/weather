# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_BBC(AbstractMeteo):
#------------------------------------------------------ Основные функции-----------------------------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'bbc'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        now = datetime.now()
        # Берем день недели на который дан прогноз
        day_forecast = '%s' % Parser('{:s}:')(re.search(r'\S*:',data.find(meteocenter.date_tag).text).group(0))
        # Сохраняем его в формате даты
        decimal_f = time.strptime(day_forecast,'%A')
        # Добавляем по дню к текущей дате до того, как она не будет равена дню из прогноза
        while now.weekday() != decimal_f.tm_wday:
            now += timedelta(days=1)

        #return now

        datestr = '%s-%s-%s %s:%s' % (now.year, now.month, now.day, ('12' if hashtag == 'max_t' else '00'), '00')
        return datetime.strptime(datestr, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('channel'):
            out = f.find('title').text
        return Parser('BBC Weather - Forecast for  {:s}, Russia')(out)    

    @classmethod
    def last_date_f(cls, last_date_f_tree, meteocenter):
        out = ''
        for f in last_date_f_tree.iter('channel'):
            out = f.find('pubDate').text
        return datetime.strptime(out, "%a, %d %b %Y %H:%M:%S +0400") # Mon, 01 Oct 2012 10:13:12 +0400
#----------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-------------------------------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        if re.search(r'Maximum Temperature:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Maximum Temperature: -?\d+')
        else:
            return -100

    @classmethod
    def min_t(cls, data, hashtag):
        if re.search(r'Minimum Temperature:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Minimum Temperature: -?\d+')
        else:
            return -100

    @classmethod
    def wind_dir(cls, data, hashtag):
        if re.search(r'Wind Direction:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Wind Direction: \S*\s?\S*\s?\S*,')
        else:
            return -100

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        if re.search(r'Wind Speed:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Wind Speed: \d+')
        else:
            return -100

    @classmethod
    def visibility(cls, data, hashtag):
        if re.search(r'Visibility:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Visibility: \S*\s?\S*,')
        else:
            return -100

    @classmethod
    def pressure_max(cls, data, hashtag):
        if re.search(r'Pressure:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Pressure: \d+')
        else:
            return -100

    @classmethod
    def humidity_max(cls, data, hashtag):
        if re.search(r'Humidity:', data.find(hashtag.m_hashtag).text):
            return cls.parse_data(data, hashtag, r'Humidity: \d+')
        else:
            return -100
#----------------------------------------------------------------------------------------------------------------------------------------------------