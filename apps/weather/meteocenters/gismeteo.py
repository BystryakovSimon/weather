# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo

class Meteo_Gismeteo(AbstractMeteo):
#------------------------------------------------------ Основные функции-----------------------------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'gismeteo'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        datestr = '%s-%s-%s %s:%s' % (data.attrib.get('year'), data.attrib.get('month'), data.attrib.get('day'), data.attrib.get('hour'), '00')
        return datetime.strptime(datestr, meteocenter.date_reg)

    @classmethod
    def last_date_f(cls, meteo_tree, meteocenter):
        f_timestep = ''
        for timestep in meteo_tree.iter(meteocenter.f_timestep):
            f_timestep = timestep

        datestr = '%s-%s-%s %s:%s' % (f_timestep.attrib.get('year'), f_timestep.attrib.get('month'), f_timestep.attrib.get('day'), f_timestep.attrib.get('hour'), '00')
        return datetime.strptime(datestr, meteocenter.date_reg)
#----------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-------------------------------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def min_t(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_dir(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def pressure_max(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def pressure_min(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def wind_velocity_min(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def humidity_max(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def humidity_min(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def heat_max(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def heat_min(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def cloud(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def falls(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)
#----------------------------------------------------------------------------------------------------------------------------------------------------