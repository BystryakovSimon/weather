# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo


class Meteo_Tiempo(AbstractMeteo):
#------------------------------------------------------ Основные функции-----------------------------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'tiempo'

    @classmethod
    def get_datetime(cls, f_timestep, meteocenter, s_timestep, hashtag):
        date = datetime.strptime(f_timestep.attrib.get('value'), '%Y%m%d')
        time = datetime.now()

        if s_timestep.attrib.get('value') == '24:00':
            time = time.replace(hour=00)
            time = time.replace(minute=00)
        else:
            time = datetime.strptime(s_timestep.attrib.get('value'), '%H:%M')

        datestr = '%s-%s-%s %s:%s' % (date.year, date.month, date.day, time.hour, time.minute)
        return datetime.strptime(datestr, meteocenter.date_reg)

#    @classmethod
#    def last_date_f(cls, last_date_f_tree, meteocenter, hashtag):
#
#        date = datetime.strptime(last_date_f_tree.attrib.get('value'), "%Y%m%d") #20130511
#
#        for f in last_date_f_tree.iter('day'):
#            time = datetime.strptime(f.find('hour').attrib.get('value'), "%H:%M")
#
#        out = '%s-%s-%s %s:%s' % (date.year, date.month, date.day, time.hour, time.minute)
#
#        return datetime.strptime(out, "%Y-%m-%dT%H:%M:%S")

#--------------------------------------------------------------------------------------------
    @classmethod
    def last_date_f(cls, meteo_tree, meteocenter):
        f_timestep = ''
        s_timestep = ''

        for timestep in meteo_tree.iter(meteocenter.f_timestep):
            f_timestep = timestep.attrib.get('value')

        date = datetime.strptime(f_timestep, '%Y%m%d')
        time = datetime.now()

        date.strftime("%d-%m-%Y %H:%M")

        for timestep in meteo_tree.iter(meteocenter.s_timestep):
#            s_timestep = datetime.strptime(timestep.attrib.get('value'), '%H:%M')
            s_timestep = timestep

        if s_timestep.attrib.get('value') == '24:00':
            time = time.replace(hour=00)
            time = time.replace(minute=00)
        else:
            time = datetime.strptime(s_timestep.attrib.get('value'), '%H:%M')

        datestr = '%s-%s-%s %s:%s' % (date.year, date.month, date.day, time.hour, time.minute)
        return datetime.strptime(datestr, meteocenter.date_reg)
#--------------------------------------------------------------------------------------------

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('location'):
            out = f.attrib.get('city')
            out = Parser('{:s} [{_:s};{_:s}]')(out)
        return out

#----------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-------------------------------------------------------------------------

    @classmethod
    def max_t(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)

    @classmethod
    def min_t(cls, data, hashtag):
        return cls.get_attr_data(data, hashtag)