# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta

import time
import re
from weather.stringparser import Parser

from weather.meteocenters.abstract import AbstractMeteo


class Meteo_Meteonova(AbstractMeteo):

#------------------------------------------------------ Основные функции---------------------------------------------------------
	@classmethod
	def is_register_for(cls, meteocenter):
		return meteocenter == 'meteonova'

	@classmethod
	def get_datetime(cls, data, meteocenter, s_timestep, hashtag):
		datestr = '%s-%s-%s %s:%s' % (data.attrib.get('year'), data.attrib.get('month'), data.attrib.get('day'), data.attrib.get('hour'), '00')
		return datetime.strptime(datestr, meteocenter.date_reg)

	@classmethod
	def get_meteo_town_name(cls, meteo_tree):
		for f in meteo_tree.iter('TOWN'):
			out = f.attrib.get('name')
		return out

	@classmethod
	def last_date_f(cls, meteo_tree, meteocenter):
		datestr = ''
		for f in meteo_tree.iter('FORECAST'):
			datestr = '%s-%s-%s %s:%s' % (f.attrib.get('year'), f.attrib.get('month'), f.attrib.get('day'), f.attrib.get('hour'), '00')
		return datetime.strptime(datestr, meteocenter.date_reg)
#--------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------- Функции получения данных-----------------------------------------------------
	@classmethod
	def max_t(cls, data, hashtag):
		return cls.get_attr_data(data, hashtag)

	@classmethod
	def min_t(cls, data, hashtag):
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
	def wind_dir(cls, data, hashtag):
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
#--------------------------------------------------------------------------------------------------------------------------------