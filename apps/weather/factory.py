# -*- coding: utf-8 -*-

from weather.meteocenters.abstract          import AbstractMeteo

from weather.meteocenters.bbc               import Meteo_BBC
from weather.meteocenters.gismeteo          import Meteo_Gismeteo
from weather.meteocenters.meteoinfo         import Meteo_Meteoinfo
from weather.meteocenters.meteonova         import Meteo_Meteonova
from weather.meteocenters.rp5               import Meteo_RP5
from weather.meteocenters.theweathernetwork import Meteo_TheWeatherNetWork
from weather.meteocenters.tiempo            import Meteo_Tiempo
from weather.meteocenters.wunderground      import Meteo_Wunderground
from weather.meteocenters.yandex_hour       import Meteo_Yandex_hour
from weather.meteocenters.yandex_day_part   import Meteo_Yandex_day_part
from weather.meteocenters.yr                import Meteo_Yr
from weather.meteocenters.current_weather   import Meteo_CurrentWeather

def MeteoModel(meteo):
	for cls in AbstractMeteo.__subclasses__():
		if cls.is_register_for(meteo):
			return cls()

	raise ValueError