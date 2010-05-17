from django.db.models import Count
from datetime  import datetime, time
from rundb_django.rundb.models import Rundbruns
from django.template import RequestContext, loader
import logging

def search_runs(data, request):
    runs = Rundbruns.objects
    runs.annotate(files_count=Count('rundbfiles'))
    none_keys = ['runid_min', 'runid_max', 'fillid_min', 'fillid_max', 'partitions',
            'runtypes', 'destinations', 'activities', 'beamenergy', 'startdate',
            'starttime', 'enddate', 'endtime', 'velo_position', 'magnet_state']
    for key in none_keys:
        data.setdefault(key)
    data.setdefault('pinned', 0)
    data.setdefault('is_show_stat', True)
    data.setdefault('onpage', 10)

    if data['runid_min'] and \
                                         not data['runid_max']:
        runs = runs.filter(runid=data['runid_min'])
    else:
        if data['fillid_min'] and \
                                        not data['fillid_max']:
            runs = runs.filter(fillid=data['fillid_min'])
        
        if data['runid_min'] and \
                                            data['runid_max']:
            runs = runs.filter(runid__gte=data['runid_min'])
        if data['runid_max']:
            runs = runs.filter(runid__lte=data['runid_max'])
        
        if data['fillid_min'] and \
                                            data['fillid_max']:
            runs = runs.filter(fillid__gte=data['fillid_min'])
            runs = runs.filter(fillid__lte=data['fillid_max'])
            
        
        if data['partitions']:
            runs = runs.filter(partitionname=
                                        data['partitions'])
        if data['runtypes']:
            runs = runs.filter(runtype=data['runtypes'])
        if data['destinations']:
            runs = runs.filter(
                              destination=data['destinations']
                               )
        if data['activities']:
            runs = runs.filter(activity=data['activities'])

        if data['beamenergy']:
            runs = runs.filter(
                    beamenergy__gte=data['beamenergy'] - 1)                
            runs = runs.filter(
                    beamenergy__lte=data['beamenergy'] + 1)
      
        if data['pinned'] == 1:
            runs = runs.filter(rundbfiles__refcount__gt=0).distinct()
      
        if (request.user.is_authenticated()) and (
                                        data['pinned'] == 2):
            runs = runs.filter(rundbfiles__refowner=request.user.username).\
                                                                    distinct()

      
        if data['startdate']:
            starttime = datetime.combine(
                        data['startdate'], time.min)
            if data['starttime']:
                starttime = datetime.combine(starttime,
                                            data['starttime'])
            runs = runs.filter(starttime__gte=starttime)
        else:
            if data['starttime']:
                starttime = datetime.combine(datetime.now(),
                                             data['starttime'])
                runs = runs.filter(starttime__gte=starttime)
      
        if data['enddate']:
            endtime = datetime.combine(
                            data['enddate'], time.max)
            if data['endtime']:
                endtime = datetime.combine(endtime,
                                            data['endtime'])
            runs = runs.filter(endtime__lte=endtime)
        else:
            if data['endtime']:
                endtime = datetime.combine(datetime.now(),
                                            data['endtime'])
                runs = runs.filter(endtime__gte=endtime)
        
        if data['velo_position']:
            runs = runs.filter(rundbrunparams__name='veloPosition',
              rundbrunparams__value__iregex=
                                        data['velo_position'])
        
        if data['magnet_state']:
            runs = runs.filter(rundbrunparams__name='magnetState',
              rundbrunparams__value__iregex=
                                        data['magnet_state'])
        
        
    counters = None
    if data['is_show_stat'] :
        counters = Rundbruns.file_counters_stat(runs)
    logging.error(runs._as_sql())    
    tpl = loader.get_template('rundb/rundb_maintable.html')
    ctx = RequestContext(request,
                               {'counters':counters, 'runs': runs.all().
                              order_by('-runid')[0:data['onpage']]})
    
    return tpl.render(ctx)
