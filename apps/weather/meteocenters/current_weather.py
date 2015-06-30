# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_CurrentWeather(AbstractMeteo):

#------------------------------------------------------ Основные функции---------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'current_weather'

    @classmethod
    def get_datetime(cls, f_timestep, meteocenter, s_timestep, hashtag):
        return datetime.strptime(f_timestep.find(meteocenter.date_tag).text, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('{http://weather.yandex.ru/forecast}forecast'):
            out = f.attrib.get('city')

        return out

    @classmethod
    def last_date_f(cls, meteo_tree, meteocenter):
        out = ''
        for f in meteo_tree.iter('{http://weather.yandex.ru/forecast}fact'):
            out = f.find('{http://weather.yandex.ru/forecast}observation_time').text
        return datetime.strptime(out, "%Y-%m-%dT%H:%M:%S")
#--------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-----------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def weather_condition(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_dir(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def humidity_max(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def pressure_max(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)
#--------------------------------------------------------------------------------------------------------------------------------