from weather.models import *
from django.contrib import admin
from models import TimeUpdate
#from django.celery.models import *
#from celery.schedules import crontab, periodictasks
#from celery.task import periodic_task
#from celery.task import task


class ProvideDataAdmin(admin.ModelAdmin):
    list_filter  = ('active', 'meteocenter', 'g_hashtag',)
    list_display = ('meteocenter', 'g_hashtag', 'active',)

    def queryset(self, request):
         return ProvideData.alls


class TownAdmin(admin.ModelAdmin):
    list_filter  = ('active', 'region',)
    list_display = ('name', 'region', 'active',)

    def queryset(self, request):
         return Town.alls


class MeteoCenterAdmin(admin.ModelAdmin):
    list_filter  = ('active', 'country', )
    list_display = ('name', 'showing_name', 'country', 'xml', 'active',)

    def queryset(self, request):
         return MeteoCenter.alls


class Town_MeteoCenterAdmin(admin.ModelAdmin):
    list_filter  = ('active', 'town', 'meteocenter', )
    list_display = ('town', 'meteocenter', 'id_of_town', 'last_date_f', 'on_main', 'active',)

    def queryset(self, request):
         return Town_MeteoCenter.alls


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'capital_id', 'active',)

    def queryset(self, request):
         return Region.alls


class TimeUpdateAdmin(admin.ModelAdmin):
    list_filter  = ('active', 'meteocenter',)
    list_display = ('meteocenter', 'time_update', 'time_indent', 'active',)

    def queryset(self, request):
         return TimeUpdate.alls


class GeneralHashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'g_hashtag', 'active',)

    def queryset(self, request):
         return GeneralHashtag.alls


class WLogAdmin(admin.ModelAdmin):
    list_filter  = ('date_record', 'town_meteo__town', 'town_meteo__meteocenter', 'time_update_meteo', 'meteo_update', 'data_update',)
    list_display = ('date_record', 'town', 'meteocenter', 'time_update_meteo', 'meteo_update', 'data_update',)

    def time_update_meteo(self, obj):
        return obj.time_update_meteo.time_update

    def town(self, obj):
        return obj.town_meteo.town

    def meteocenter(self, obj):
        return obj.town_meteo.meteocenter


class WDataAdmin(admin.ModelAdmin):
    list_filter = ('town_meteo__town', 'g_hashtag', 'town_meteo__meteocenter', 'time', 'date_f', 'd_data_upd',)
    #list_display = ('__unicode__', )#'town', 'meteocenter', 'date_f', 'g_hashtag', 'data')# self.town, self.meteocenter, self.date_f, self.g_hashtag, self.data
    list_display = ('town', 'meteocenter', 'date_f', 'g_hashtag', 'data', 'd_data_upd',)

    def town(self, obj):
        return obj.town_meteo.town

    def meteocenter(self, obj):
        return obj.town_meteo.meteocenter


admin.site.register(Region, RegionAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(MeteoCenter, MeteoCenterAdmin)
admin.site.register(Town_MeteoCenter, Town_MeteoCenterAdmin)
admin.site.register(TimeUpdate, TimeUpdateAdmin)
admin.site.register(GeneralHashtag, GeneralHashtagAdmin)
admin.site.register(ProvideData, ProvideDataAdmin)
admin.site.register(WData, WDataAdmin)
admin.site.register(WLog, WLogAdmin)