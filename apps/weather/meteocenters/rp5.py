# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_RP5(AbstractMeteo):
#------------------------------------------------------ Основные функции---------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'rp5'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        return datetime.strptime(data.find(meteocenter.date_tag).text, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('point'):
            out = f.find('point_name').text
        return out

#    @classmethod
#    def last_date_f(cls, last_date_f_tree, meteocenter, hashtag):
#        for f in last_date_f_tree.iter('point'):
#            out = f.find('point_date_time').text
#        return datetime.strptime(out, "%Y-%m-%d %H:%M ")
#--------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-----------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def cloud(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

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
    def precipitation(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)

    @classmethod
    def falls(cls, data, hashtag):
        return cls.get_text_data(data, hashtag)
#--------------------------------------------------------------------------------------------------------------------------------