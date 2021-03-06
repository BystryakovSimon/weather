# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'htdocs.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'htdocs.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for htdocs.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_(u'Собрать данные'), '/get_datas'],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(
            modules.ModelList(
                title = u'Пользователи',
                models=(
                    'django.contrib.auth.*',
                    'my_accounts.models.Profile',
                ),
            )
        )
        self.children.append(modules.Group(

            title=u"Управление сайтом",
            display="accordion",
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                modules.ModelList(
                    title=u'Djcelery',
                    models=(
                        'djcelery.models.CrontabSchedule',
                        'djcelery.models.IntervalSchedule',
                        'djcelery.models.PeriodicTasks',
                        'djcelery.models.TaskState',
                        'djcelery.models.WorkerState',)
                ),
                modules.ModelList(
                    title=u'Djkombu',
                    models=(
                        'djkombu.models.Message',
                        'djkombu.models.Queue',)
                ),
                modules.ModelList(
                    title=u'CMS',
                    models=(                    
                        'cms.models.pagemodel.Page',
                        'cms.plugins.snippet.models.Snippet',)
                ),
                modules.ModelList(
                    title=u'Пользователи',
                    models=(
                        'django.contrib.auth.*',
                        'my_accounts.models.Profile',)
                ),
            ]
        ))

        self.children.append(modules.Group(

            title=u"RateForecast",
            display="accordion",
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                modules.ModelList(
#                    title=u'RateForecast',
                    models=(
                        'weather.models.Region',
                        'weather.models.Town',
                        'weather.models.MeteoCenter',
                        'weather.models.Town_MeteoCenter',
                        'weather.models.TimeUpdate',
                        'weather.models.GeneralHashtag',
                        'weather.models.ProvideData',
                        'weather.models.WData',
                        'weather.models.WLog',)
                ),
            ]
        ))

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for htdocs.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
