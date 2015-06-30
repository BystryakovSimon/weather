# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_Yandex_hour(AbstractMeteo):

#------------------------------------------------------ Основные функции---------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'yandex_hour'

    @classmethod
    def get_datetime(cls, f_timestep, meteocenter, s_timestep, hashtag):
        date = datetime.strptime(f_timestep.attrib.get('date'), '%Y-%m-%d')
        time = datetime.strptime(s_timestep.attrib.get('at'), '%H')

        datestr = '%s-%s-%s %s:%s' % (date.year, date.month, date.day, time.hour, '00')
        return datetime.strptime(datestr, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('{http://weather.yandex.ru/forecast}fact'):
            out = f.find('{http://weather.yandex.ru/forecast}station').text
        return out

    @classmethod
    def last_date_f(cls, last_date_f_tree, meteocenter, hashtag):
        for f in last_date_f_tree.iter('{http://weather.yandex.ru/forecast}fact'):
            out = f.find('{http://weather.yandex.ru/forecast}observation_time').text
        return datetime.strptime(out, "%Y-%m-%dT%H:%M:%S")
#--------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-----------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def min_t(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)
#--------------------------------------------------------------------------------------------------------------------------------