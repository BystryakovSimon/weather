# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from lib.decorators import wind_direct

import time
import re
import pytz
from weather.stringparser import Parser

class AbstractMeteo(object):
    @classmethod
    def get_data(cls, data, hashtag):
        if hasattr(cls, hashtag.g_hashtag.g_hashtag):
            return getattr(cls, hashtag.g_hashtag.g_hashtag)(data, hashtag)
        return -100

    @classmethod
    def get_text_data(cls, data, hashtag):
        return data.find(hashtag.m_hashtag).text

    @classmethod
    def get_attr_data(cls, data, hashtag):
        return data.find(hashtag.m_hashtag).attrib.get(hashtag.m_hashtag_attr)

    @classmethod
    def parse_data(cls, data, hashtag, find):
        # find- нужное совпадение в тексте тега в виде регулярного выражения (пример: r'Maximum Temperature: \d+')
        return Parser(hashtag.m_hashtag_desc)(re.search(find, data.find(hashtag.m_hashtag).text).group())

    @classmethod
    def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
        return datetime.now()

    # Возвращает название города из метеоцентра
    @classmethod
    def get_meteo_town_name(cls, meteo_tree):
        return False

    # Дата последнего обновления данных
    # если у метеоцентра нет pubDate - дата последнего прогноза
    @classmethod
    def last_date_f(cls, last_date_f_tree, meteocenter):

#
#        if not hashtag.s_timestep:
#            fs_array = [(f, 0) for f in meteo_tree.iter(meteocenter.f_timestep)]
#        else:
#            fs_array = [(f, s) for f in meteo_tree.iter(meteocenter.f_timestep) for s in f.iter(meteocenter.s_timestep)]
#

        # Берем последнюю дату на которую был дан прогноз
#        for f_timestep, s_timestep in fs_array:
#            cur_last_date_f = cls.get_datetime(f_timestep, meteocenter, s_timestep, hashtag)

#        return cur_last_date_f

        return datetime.now()