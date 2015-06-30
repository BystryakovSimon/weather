# -*- coding: utf-8 -*-
from datetime import datetime

import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_Yr(AbstractMeteo):
#------------------------------------------------------ Основные функции---------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'yr'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        return datetime.strptime(data.attrib.get('from'), meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('name'):
            out = f.text
        return out

    @classmethod
    def last_date_f(cls, last_date_f_tree, meteocenter):
        for f in last_date_f_tree.iter('meta'):
            out = f.find('lastupdate').text
        return datetime.strptime(out, "%Y-%m-%dT%H:%M:%S")
#--------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-----------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def precipitation(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_dir(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def pressure_max(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def cloud(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)
#--------------------------------------------------------------------------------------------------------------------------------