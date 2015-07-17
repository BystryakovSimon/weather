# -*- coding: utf-8 -*-
"""
WSGI config for mysite project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

#import os, sys
#virtual_env = os.path.expanduser('~/home/lobach/lobachEnv')
#activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
#execfile(activate_this, dict(__file__=activate_this))
#sys.path.insert(0, os.path.join(os.path.expanduser('~'), '/home/lobach/lobach'))
#sys.path.insert(0, os.path.join(os.path.expanduser('~'), '/home/lobach'))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

logto = "/home/uwsgi_log/UWSGI.log"
