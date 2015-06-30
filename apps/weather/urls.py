from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('weather.views'
	, url(r'^$', 'main')
    , url(r'^get_datas/$', 'get_datas')
	, url(r'^(?P<town_url>\S*)/full7/$', 'town_full7')
    , url(r'^(?P<town_url>\S*)/full3/$', 'town_full3')
    , url(r'^(?P<town_url>\S*)/full/$' , 'town_full')
    , url(r'^(?P<town_url>\S*)/$'      , 'town_preview')
)