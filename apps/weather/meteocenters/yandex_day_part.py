# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_Yandex_day_part(AbstractMeteo):

#------------------------------------------------------ Основные функции---------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'yandex_day_part'

    @classmethod
    def get_datetime(cls, f_timestep, meteocenter, s_timestep, hashtag):
        date = datetime.strptime(f_timestep.attrib.get(meteocenter.date_tag), '%Y-%m-%d')
        time = datetime.strptime(s_timestep.attrib.get('typeid'), '%H')

        datestr = '%s-%s-%s %s:%s' % (date.year, date.month, date.day, time.hour, '00')
        return datetime.strptime(datestr, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('{http://weather.yandex.ru/forecast}forecast'):
            out = f.attrib.get('city')

        return out

    @classmethod
    def last_date_f(cls, meteo_tree, meteocenter, fs_array, hashtag):
        for f in meteo_tree.iter('{http://weather.yandex.ru/forecast}fact'):
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

    @classmethod
    def weather_condition(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_direction(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def wind_speed(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def humidity(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def mslp_pressure(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)
#--------------------------------------------------------------------------------------------------------------------------------