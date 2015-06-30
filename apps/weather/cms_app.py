# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class MainApp(CMSApp):
    name = _(u"Главная")
    urls = ["weather.urls"] 

apphook_pool.register(MainApp)