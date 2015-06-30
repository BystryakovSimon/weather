# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime, timedelta
from django.db.models import Q

now = datetime.now()

# Менеджер для рагионов
class RegionManager(models.Manager):
    def get_query_set(self):
        return super(RegionManager, self).get_query_set().filter(active=True)

    def capital(self):
        return self

# Регион
class Region(models.Model):
    active     = models.BooleanField('Активный', default=True)
    name       = models.CharField('Название', max_length=100)
    flag_small = models.ImageField('Флаг(маленький)',  upload_to="images/flags/regions/")
    flag_big   = models.ImageField('Флаг(большой)',  upload_to="images/flags/regions/")
    capital_id = models.IntegerField('id столицы региона', default=0)

    objects    = RegionManager()
    alls       = models.Manager()

    class Meta:
        verbose_name        = 'Регион'
        verbose_name_plural = 'Регионы'
        ordering            = ['id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return self.name

    @property
    def capital(self):
#        try:
        return self#.get_towns.all()#.filter(id=self.capital_id)
#        except:
#            return 1


# Менеджер для городов
class TownManager(models.Manager):
    def get_query_set(self):
        return super(TownManager, self).get_query_set().filter(active=True)

# Город
class Town(models.Model):
    active     = models.BooleanField('Активный', default=True)
    name       = models.CharField('Название', max_length=100)
    town_url   = models.CharField('url города', max_length=100)
    flag_small = models.ImageField('Флаг(маленький)',  upload_to="images/flags/towns/")
    flag_big   = models.ImageField('Флаг(большой)', upload_to="images/flags/towns/")
    geo        = models.CharField('Координаты города', max_length=50)
    region     = models.ForeignKey(Region, verbose_name="Регион", related_name="get_towns")

    objects    = TownManager()
    alls       = models.Manager()

    class Meta:
        verbose_name        = 'Город'
        verbose_name_plural = 'Города'
        ordering            = ['id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return self.name


# Менеджер для метеоцентров
class MeteoCenterManager(models.Manager):
    def get_query_set(self):
        return super(MeteoCenterManager, self).get_query_set().filter(active=True)

# Метеоцентр
class MeteoCenter(models.Model):
    active       = models.BooleanField('Активный', default=True)
    name         = models.CharField('Название', max_length=100)
    showing_name = models.CharField('Показываемое название', max_length=100, blank=True, null=True)
    link         = models.TextField('Ссылка на метеоцентр')
    desc         = models.TextField('Описание метеоцентра')
    country      = models.CharField('Страна', max_length=100)
    flag         = models.ImageField('Флаг страны',  upload_to="images/flags/country/")
    xml          = models.TextField('Строка линка(XML)')
    f_timestep   = models.CharField('Временной шаг первого уровня', max_length=100)
    s_timestep   = models.CharField('Временной шаг второго уровня', max_length=100, blank=True, null=True)
    date_tag     = models.CharField('Тег даты(атрибут)', max_length=100, blank=True, null=True)
    date_reg     = models.CharField('Регуляторное выражение даты', max_length=100, blank=True, null=True)

    objects    = MeteoCenterManager()
    alls       = models.Manager()

    class Meta:
        verbose_name        = 'Метеорологический центр'
        verbose_name_plural = 'Метеорологические центры'
        ordering            = ['id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return self.name


# Менеджер для Город- Метеоцентр
class Town_MeteoCenterManager(models.Manager):
    def get_query_set(self):
        return super(Town_MeteoCenterManager, self).get_query_set().filter(active=True, town__active=True, meteocenter__active=True)

# Связь двух таблиц Город- Метеоцентр
class Town_MeteoCenter(models.Model):
    active          = models.BooleanField('Активный', default=True)
    town            = models.ForeignKey(Town, verbose_name="Город", related_name="get_meteocenters",)
    meteocenter     = models.ForeignKey(MeteoCenter, verbose_name="Метеоцентр", related_name="get_t_m",)
    id_of_town      = models.CharField('id города в url', max_length=100)
    last_date_f     = models.DateTimeField('Дата и время  последнего прогноза', blank=True, null=True)
    meteo_town_name = models.CharField('Название города в метеоцентре', max_length=100, blank=True, null=True)
    on_main         = models.BooleanField('Отображать на главной странице', default=True)
    
    objects         = Town_MeteoCenterManager()
    alls            = models.Manager()

    class Meta:
        verbose_name        = 'Город - Метеорологический центр'
        verbose_name_plural = 'Города - Метеорологические центры'
        ordering            = ['id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return u'%s_%s' % (self.town.town_url, self.meteocenter)


# Менеджер для времени сбора обновленных данных на каждом метеоцентре 
class TimeUpdateManager(models.Manager):
    def get_query_set(self):
        return super(TimeUpdateManager, self).get_query_set().filter(active=True)

# Время сбора обновленных данных на каждом метеоцентре, 
# время отступа сбора данных для крон-демона
class TimeUpdate(models.Model):
    active      = models.BooleanField('Активный', default=True)
    meteocenter = models.ForeignKey(MeteoCenter, verbose_name="Метеоцентр", related_name="get_tu")
    time_update = models.TimeField('Время сбора')
    time_indent = models.TimeField('Время отхождения')
    count       = models.IntegerField('Кол-во раз не обновления метеоцентра во время', blank=True, null=True, default=0)

    objects     = TimeUpdateManager()
    alls        = models.Manager()

    class Meta:
        verbose_name        = 'Дата обновления'
        verbose_name_plural = 'Даты обновления'
        ordering            = ['id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return u'%s- %s' % (self.meteocenter, self.time_update)


# Менеджер для общих хештегов
class GeneralHashtagManager(models.Manager):
    def get_query_set(self):
        return super(GeneralHashtagManager, self).get_query_set().filter(active=True)

# Общий хэштег. Один хэштег для разных хэштегов каждого метеоцентра
class GeneralHashtag(models.Model):
    active    = models.BooleanField('Активный', default=True)
    name      = models.CharField('Название', max_length=100)
    g_hashtag = models.CharField('Общий хэштег', max_length=100)

    objects   = GeneralHashtagManager()
    alls      = models.Manager()

    class Meta:
        verbose_name        = 'Общий хэштег'
        verbose_name_plural = 'Общие хэштеги'
        ordering            = ['id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return self.name


# Менеджер для предоставляемых данных
class ProvideDataManager(models.Manager):
    def get_query_set(self):
        return super(ProvideDataManager, self).get_query_set().filter(active=True)

# Таблица для сапоcтавления хэштега метеоцентра и общего хэштега
class ProvideData(models.Model):
    active         = models.BooleanField('Активный', default=True)
    meteocenter    = models.ForeignKey(MeteoCenter, verbose_name="Метеоцентр", related_name="get_gm_hashtags")
    g_hashtag      = models.ForeignKey(GeneralHashtag, verbose_name="Общий хэштег", related_name="get_mc_hashtags")
    m_hashtag      = models.CharField('Хэштег метеоцентра', max_length=100)
    s_timestep     = models.BooleanField('Хэштег находится на втором уровне временного шага')
    m_hashtag_attr = models.CharField('Атрибут хэштега метеоцентра', max_length=100, blank=True, null=True)
    m_hashtag_desc = models.TextField('Данные в тексте одного тега(description)', blank=True, null=True)
    
    objects        = ProvideDataManager()
    alls           = models.Manager()

    class Meta:
        verbose_name        = 'Предоставляемые данные'
        verbose_name_plural = 'Предоставляемые данные'
        ordering            = ['meteocenter']
        get_latest_by       = "-id"

    def __unicode__(self):
        return u'%s - %s' % (self.meteocenter, self.g_hashtag)


# Менеджер для WData
class TransactionManager(models.Manager):
    def get_query_set(self):
        return WDataManager(self.model)

class WDataManager(models.query.QuerySet):

    def get_lastest_data(self, town_meteo, date, g_hashtag):
        try:
            a = self.filter_by_t_m(town_meteo).filter_by_day(date).filter_by_g_hashtag(g_hashtag)
        except Exception as e:
            print 'get_lastest_data Exception - %s' %e
            a = ''
        return a

    def filter_by_g_hashtag(self, g_hashtag):
        try:
            a = self.filter(g_hashtag__g_hashtag=g_hashtag)
        except Exception as e:
            print 'filter_by_g_hashtag Exception - %s' %e
            a = ''
        return a

    def filter_by_hour(self):
        try:
            a = self.filter(date_f__gt=now)
        except Exception as e:
            print 'filter_by_hour Exception - %s' %e
            a = self
        return a

    def filter_by_day(self, date):
        try:
            a = self.filter(
                    date_f__year=date.year
                    , date_f__month=date.month
                    , date_f__day=date.day
                )
            last_forecast = a.order_by("-d_data_upd")
            #last_forecast      = a.filter(d_data_upd=date_last_forecast).order_by("date_f")
        except Exception as e:
            print 'filter_by_day Exception (%s)- %s' %(date, e)
            last_forecast = ''
        return last_forecast

    def filter_by_town(self, town):
        try:
            a = WData.objects.filter(town_meteo__town=town)
        except Exception as e:
            print 'filter_by_town Exception - %s' %e
            a = ''
        return a

    def filter_by_t_m(self, town_meteocenter):
        try:
            a = self.filter(town_meteo=town_meteocenter)
        except Exception as e:
            print 'filter_by_t_m Exception - %s' %e
            a = ''
        return a

    def filter_by_time(self, time_from, time_to):
        data = None
#        self = self.order_by('d_data_upd')
        for self_datas in self:
            if (self_datas.date_f >= time_from) and (self_datas.date_f <= time_to):
                data = self_datas.data
        return data

    def filter_by_range_of_time(self, time_from, time_to):
        hour = 0
        data = None
        while(data == None and hour<24):
            for self_datas in self:
                if (self_datas.date_f >= (time_from - timedelta(hours=hour))) and (self_datas.date_f <= time_to):
                    data = self_datas.data
            #data = data.filter_by_time(time_from - timedelta(hours=hour), time_to)
            hour += 6
        return data

# Все погодные данные на определенную дату и время WData
class WData(models.Model):
    town_meteo  = models.ForeignKey(Town_MeteoCenter, verbose_name="Город-Метеоцентр", related_name="get_datas_by_tm")
    time        = models.ForeignKey(TimeUpdate, verbose_name="Дата обновления", related_name="get_datas_by_tu")
    g_hashtag   = models.ForeignKey(GeneralHashtag, verbose_name="Общий хэштег", related_name="get_datas_by_gh")
    date_f      = models.DateTimeField('Дата и время прогноза')
    data        = models.CharField('Данные', max_length=255)
    d_data_upd  = models.DateTimeField('Дата получения данных', default=now)

    objects     = TransactionManager()

    class Meta:
        verbose_name        = 'Данные'
        verbose_name_plural = 'Данные'
        ordering            = ['-id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return u'%s - %s, Дата прогноза- %s, время прогноза- %s, %s - %s' % (self.town_meteo.town, self.town_meteo.meteocenter, self.date_f.strftime("%d-%m-%Y"), self.date_f.strftime("%H:%M"), self.g_hashtag, self.data)


# Логирование
class WLog(models.Model):
    date_record       = models.DateTimeField('Дата и время записи', default=now)
    town_meteo        = models.ForeignKey(Town_MeteoCenter, verbose_name="Город-Метеоцентр", related_name="get_wlogs_by_tm")
    time_update_meteo = models.ForeignKey(TimeUpdate, verbose_name="Дата обновления метеоцентра", related_name="get_wlogs_by_tu")
    meteo_update      = models.BooleanField('Предоставляемые даные обновлены', default=False)
    data_update       = models.BooleanField('Все данные успешно добавлены в базу', default=False)
    error             = models.TextField('Ошибка', blank=True, null=True)

    class Meta:
        verbose_name        = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering            = ['-id']
        get_latest_by       = "-id"

    def __unicode__(self):
        return u'%s, %s - %s, %s' % (self.date_record.strftime("%d-%m-%Y %H:%M"), self.town_meteo.meteocenter, self.time_update_meteo.time_update, self.town_meteo.town)
