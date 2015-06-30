
    # Последние 7 дней
    start_date = datetime.now() - timedelta(days=7)
    end_date   = datetime.now()

    #a = start_date
    #queryset = wdata
    #while a != end_date:
        # 1 - town_meteo, a - date
    #queryset = wdata.get_lastest_data(1, a)
    #    a += timedelta(days=1)

#int(WData.objects.all().data)

#    qsstats = QuerySetStats(queryset, date_field='date_f', aggregate=int(WData.data))  

    
    #WData = WData()   -?\d+
    rp5 = WData.objects.filter(town_meteo__meteocenter__name='rp5', town_meteo__town__id=town.id, g_hashtag_id=1,)

    #rp5_data = []
    #for p in rp5:
    #    rp5_data.append(int(p.data))
    #    print u'p.data - %s' %p.data
    #   print u'rp5_data - %s' %rp5_data


    #gis = WData.objects.filter(town_meteo__meteocenter__name='gismeteo', town_meteo__town__id=town.id, g_hashtag_id=1,)
    # -----------------------------------------------------------------------------------------------------------------------------------
    #rp5 = re.search(r'*-?\d+', WData.objects.filter(town_meteo__meteocenter='rp5',      town_meteo__town__id=town.id, g_hashtag_id=1,).data).group()
    #gis = re.search(r'*-?\d+', WData.objects.filter(town_meteo__meteocenter='gismeteo', town_meteo__town__id=town.id, g_hashtag_id=1,).data).group()

    #rp5 = WData.objects.filter(town_meteo__meteocenter='rp5',      town_meteo__town__id=town.id, g_hashtag_id=1,).data
    #gis = WData.objects.filter(town_meteo__meteocenter='gismeteo', town_meteo__town__id=town.id, g_hashtag_id=1,).data


    #out['gr_data'] = qsstats.QuerySetStats('date_f', rp5, gis).time_series(start_date, end_date)


    #  django google chars
    #queryset = WData.objects.all()
    #rp5 = WData.objects.filter(town_meteo__meteocenter__name='rp5',      town_meteo__town__id=town.id, g_hashtag_id=1,)
    #gis = WData.objects.filter(town_meteo__meteocenter__name='gismeteo', town_meteo__town__id=town.id, g_hashtag_id=1,)

    #qsstats       = qsstats.QuerySetStats(rp5, date_field='date_f', aggregate=Count('id'))
    #gr_rp5        = QuerySetStats(rp5, date_field='date_f', aggregate=Count('data'))
    #out['gr_rp5'] = gr_rp5.time_series(start_date, end_date, interval='days')

    #gr_gis        = QuerySetStats(gis, date_field='date_f', aggregate=Count('id'))
    #out['gr_gis'] = gr_gis.time_series(start_date, end_date, interval='days')

    #qs = User.objects.all()
    #qss = qsstats.QuerySetStats(qs, 'date_joined')

    #date = datetime.now() - timedelta(days=7)
    #gr_tuple = () # кортеж для графика
    #for a in xrange(7):
    #    gr_list    = [] # список для графика
    #    gr_list[0] = date.day
    #    gr_list[1] = WData.objects.filter(town_meteo__meteocenter__name='rp5',      town_meteo__town__id=town.id, g_hashtag_id=1, date_f__day=date.day,)[0]
    #    gr_list[2] = WData.objects.filter(town_meteo__meteocenter__name='gismeteo', town_meteo__town__id=town.id, g_hashtag_id=1, date_f__day=date.day,)[0]
    #    gr_tuple  += gr_list
    #    date      += timedelta(days=1)

    #data = QuerySetStats(qs, 'date_joined').time_series(start, end)
    #values = [t[1] for t in data]
    #captions = [t[0].day for t in data]

    #out['gr_tuple'] = gr_tuple    
