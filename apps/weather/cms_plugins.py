# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from weather.graphic import gr_data


class CMS3DaysGrPlugin(CMSPluginBase):
    name = _(u"Трех дневный график")
    render_template = "3day_gr.html"

    def render(self, context, instance, placeholder):
        context.update({
        	'3days_gr_forecasts' : gr_data(context['request'].session.get('all_data_for_town', None), context['request'].session.get('town', None), context['request'].session.get('town_meteos', None), 3),  
            'object'             : instance,
            'placeholder'        : placeholder
        })
        return context


class CMSOneDaysGrPlugin(CMSPluginBase):
    name = _(u"Однодневный график")
    render_template = "day_gr.html"

    def render(self, context, instance, placeholder):
        context.update({
        	'today_gr_forecasts' : gr_data(context['request'].session.get('all_data_for_town', None), context['request'].session.get('town', None), context['request'].session.get('town_meteos', None), 2),  
            'object'             : instance,
            'placeholder'        : placeholder
        })
        return context


plugin_pool.register_plugin(CMS3DaysGrPlugin)
plugin_pool.register_plugin(CMSOneDaysGrPlugin)