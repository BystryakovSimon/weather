# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo


class Meteo_Meteoinfo(AbstractMeteo):
#------------------------------------------------------ Основные функции-----------------------------------------------------------------------------
    @classmethod
    def is_register_for(cls, meteocenter):
        return meteocenter == 'meteoinfo'

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        today   = datetime.today()
        datestr = '%s-%s-%s %s:%s' % (today.year, today.month, Parser(u'{_:s}, {:d} {_:s}')(data.find(meteocenter.date_tag).text)
            , ('12' if hashtag == 'max_t' else '00')
            , '00')
        return datetime.strptime(datestr, meteocenter.date_reg)

    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        for f in meteo_tree.iter('item'):
            out = f.find('title').text

        #return Parser(ur'{:s},{_:s}')(out)
        return re.search(u'\S*,', out).group()

    @classmethod
    def last_date_f(cls, meteo_tree, meteocenter):
        out = ''
        for f in meteo_tree.iter('item'):
            out = f.find('source').text

        print 'meteoinfo------------------------------------------------------------------------------', out
        return datetime.strptime(re.search(ur'\d+.\d+.\d+ в \d+:\d+', out).group(), u"%d.%b.%Y в %H:%M")
#----------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-------------------------------------------------------------------------
    @classmethod
    def max_t(cls, data, hashtag):
        if re.search(u'Температура', data.find(hashtag.m_hashtag).text):
            return Parser(hashtag.m_hashtag_desc)(re.search(ur'Температура ночью -?\d+°, днём -?\d+°.', data.find(hashtag.m_hashtag).text).group())
        else:
            return -100

    @classmethod
    def min_t(cls, data, hashtag):
        if re.search(u'Температура', data.find(hashtag.m_hashtag).text):
            return Parser(hashtag.m_hashtag_desc)(re.search(ur'Температура ночью -?\d+°, днём -?\d+°.', data.find(hashtag.m_hashtag).text).group())
        else:
            return -100

#    @classmethod
#    def weather_condition(cls, data, hashtag):
#        if re.search(u'', data.find(hashtag.m_hashtag).text):
#            return Parser(hashtag.m_hashtag_desc)(re.search(ur'\W* ?\W*, \W* ?\W*\. ', data.find(hashtag.m_hashtag).text).group())
#        else:
#            return -100

    @classmethod
    def weather_condition(cls, data, hashtag):
        if re.search(u'', data.find(hashtag.m_hashtag).text):
            #return Parser(hashtag.m_hashtag_desc)(re.search(ur'\W* ?\W*, \W* ?\W*\. ', data.find(hashtag.m_hashtag).text).group())
            #return cls.parse_data(data, hashtag, r'\W* ?\W*, \W* ?\W*\. ')
            return re.search(ur'\W* ?\W*, \W* ?\W*\. ', data.find(hashtag.m_hashtag).text).group()
        else:
            return -100

    @classmethod
    def wind_dir(cls, data, hashtag):
        if re.search(u'Ветер', data.find(hashtag.m_hashtag).text):
            #return Parser(hashtag.m_hashtag_desc)(re.search(ur'Ветер \S+,', data.find(hashtag.m_hashtag).text).group())
            return re.search(ur'Ветер \W*-?\W*,', data.find(hashtag.m_hashtag).text).group()
        else:
            return -100

    @classmethod
    def pressure_min(cls, data, hashtag):
        if re.search(u'Атмосферное давление ночью', data.find(hashtag.m_hashtag).text):
            return Parser(hashtag.m_hashtag_desc)(re.search(ur'Атмосферное давление ночью \d+', data.find(hashtag.m_hashtag).text).group())
        else:
            return -100

    @classmethod
    def pressure_max(cls, data, hashtag):
        if re.search(u'Атмосферное давление ночью', data.find(hashtag.m_hashtag).text):
            return Parser(hashtag.m_hashtag_desc)(re.search(ur'Атмосферное давление ночью \d+ мм рт.ст., днём \d+', data.find(hashtag.m_hashtag).text).group())
        else:
            return -100

    @classmethod
    def pop(cls, data, hashtag):
        if re.search(u'Вероятность осадков', data.find(hashtag.m_hashtag).text):
            return Parser(hashtag.m_hashtag_desc)(re.search(ur'Вероятность осадков \d+', data.find(hashtag.m_hashtag).text).group())
        else:
            return -100

    @classmethod
    def wind_velocity_max(cls, data, hashtag):
        if re.search(u'Ветер', data.find(hashtag.m_hashtag).text):
            return Parser(hashtag.m_hashtag_desc)(re.search(ur'Ветер \W*, \d+ ', data.find(hashtag.m_hashtag).text).group())
        else:
            return -100
#----------------------------------------------------------------------------------------------------------------------------------------------------