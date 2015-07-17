# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from lib.decorators import render_to
from models import WData, MeteoCenter, Town, WLog, Region
from datetime import datetime, timedelta
#from celery import shared_task

from celery import task


@task(name='weather.tasks.WParser')
#@app.task(name='settings.task.WParser')
#@periodic_task(run_every=crontab(minute=1,))
#@shared_task
def WParser():
    from weather.wparser import meteocenter_parser

    out = {}

    for meteocenter in MeteoCenter.objects.all():

        for time_update in meteocenter.get_tu.all():
            a = datetime.now()#-timedelta(minutes=30)
            #b = datetime.now()+timedelta(minutes=30)
            b = datetime.now()+timedelta(hours=1)
            if time_update.time_update>a.time() and time_update.time_update<b.time():
                meteo_time_update = time_update

                meteocenter_parser(meteocenter,meteo_time_update)