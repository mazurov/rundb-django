from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, \
                                                        HttpResponseBadRequest
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from rundb_django.rundb.models import Rundbruns, Rundbfiles, Rundbfills
from rundb_django.rundb.search_form import SearchForm, ApiForm
from rundb_django.rundb.search_runs  import search_runs
#import pprint
#import logging

def search_form(request=None):
    nomatter = ('', 'ANY')
    partitions = [nomatter] + [(partition, partition) for partition in 
                                                Rundbruns.all_partitions() 
                                                if  partition]
    runtypes = [nomatter] + [(runtype, runtype) for runtype in 
                                                Rundbruns.all_runtypes() 
                                                if runtype]
  
    destinations = [nomatter] + [(destination, destination) for destination in 
                                                Rundbruns.all_destinations() 
                                                if destination]
    activities = [nomatter] + [(activity, activity) for activity in 
                                                    Rundbruns.all_activities() 
                                                    if activity]
    return SearchForm(request.user, partitions, runtypes, destinations,
                      activities, request.POST) 


def index(request):
    return fills(request)

def search(request):
    return render_to_response('rundb/rundb_search.html',
      {'form':search_form(request)}, context_instance=RequestContext(request))

def fills(request):
    fills = Rundbfills.objects.filter(time_total__gt=0).all().\
                                                order_by('-timestamp')
    total = Rundbfills.total() 
    return render_to_response('rundb/rundb_fills.html',
      {'fills':fills,'total':total}, context_instance=RequestContext(request))
    
def fill(request, fillid):
    fill = get_object_or_404(Rundbfills, pk=fillid)
    search_data = {'fillid_min':fillid, 'partitions':'LHCb',
                   'destinations':'OFFLINE', 'onpage':100}
    return render_to_response('rundb/rundb_fill.html',
      {'fill':fill, 'fills':[fill], 'single':True, 'stat':search_runs(search_data, request)}, context_instance=RequestContext(request))


def redirect(request):
    return HttpResponseRedirect("/")

"""
Result for ajax form
"""
def maintable(request):
    form = search_form(request)
    if form.is_valid():
        json = simplejson.dumps(search_runs(form.cleaned_data, request))
    else:
        json = simplejson.dumps("form not valid" + str(form.errors))

    return HttpResponse(json, mimetype='application/json')


def files(request, runid, page=1):
    #---------------------------------------------------------------------------
    onpage = 10
    page = int(page)
    #---------------------------------------------------------------------------
    if page == 1:
        tplfile = 'rundb/rundb_files.html'
    else:
        tplfile = 'rundb/rundb_files_rows.inc.html'
    #---------------------------------------------------------------------------
    tpl = loader.get_template(tplfile)
    run = Rundbruns.objects.get(pk=runid);
    #---------------------------------------------------------------------------
    # Context
    #--------------------------------------------------------------------------
    context = {'run':run, 'files': run.rundbfiles_set.all()[(page - 1) * 
                                                        onpage:page * onpage]}
    if run.rundbfiles_set.count() > page * onpage:
        context['next'] = page + 1
    #---------------------------------------------------------------------------
    ctx = RequestContext(request, context)
    #---------------------------------------------------------------------------
    return HttpResponse(simplejson.dumps(tpl.render(ctx)),
                                                mimetype='application/json');

@login_required
def file_pin(request, fileid):
    file = get_object_or_404(Rundbfiles, pk=fileid)
    file.pin(request.user)
    file.save();
    result = simplejson.dumps({'refcount':file.refcount})
    return HttpResponse(result, mimetype='application/json')

def file_log(request, fileid):
    file = get_object_or_404(Rundbfiles, pk=fileid)
    return render_to_response('rundb/rundb_file_log.html',
      {'file':file}, context_instance=RequestContext(request))

def run(request, runid):
    run = get_object_or_404(Rundbruns, pk=runid)

    return render_to_response('rundb/rundb_run.html',
      {'single':True, 'run':run, 'runs':[run]},
      context_instance=RequestContext(request))

def file(request, fileid):
    file = get_object_or_404(Rundbfiles, pk=fileid)
    run = file.run
    return render_to_response('rundb/rundb_file.html',
                              {'single':True, 'file':file,
                               'files':[file],
                               'run':run},
                               context_instance=RequestContext(request))


def _api_response(request, result):
    """
    Creates the response object for the api_* views serializing the result as a
    JSON object.
    
    If the argument 'callback' is included in the request, the response uses the
    JSONP pattern and the argument value is used as the callback function.
    """
    callback = request.GET.get("callback")
    
    res = HttpResponse(mimetype='application/json')
    
    if callback:
        res.write("%s(" % callback)
        #res.write(json)
        simplejson.dump(result, res)
        res.write(")")
    else:
        #res.write(json)
        simplejson.dump(result, res)
    
    return res

def _api_run_as_json(run):
    """
    Creates a dictionary from a Run object so that it can be serialized with JSON
    """
    result = {}

    attrs = ('runid', 'partitionid', 'runtype', 'partitionname', 'destination')
    for a in attrs:
        result[a] = getattr(run, a)

    attrs = ('starttime', 'endtime')
    for a in attrs:
        result[a] = getattr(run, a).strftime("%Y-%m-%dT%H:%M:%S%z")

    result['state'] = run.state
    return result


def api_run(request, runid):
    """
    Returns the information of a Run in JSON format.

    Query arguments are (optional):

    - callback: The response will use the JSONP format. The argument is used as
        the name of the callback function.

    """
    run = get_object_or_404(Rundbruns, pk=runid)
    result = _api_run_as_json(run)

    return _api_response(request, result)

def api_search(request):
    """
    Search the run database and returns the results ordered by run number
    using JSON format.

    Query arguments are (optional):

     - starttime: In format 2009-11-02T112:57:00
     - endtime: In format 2009-11-02T112:57:00
     - destination
     - partition
     - start: First result (0 based)
     - rows: Maximum number of results
     - callback: The response will use the JSONP format. The argument is used as
        the name of the callback function.

    """
    form = ApiForm(request.GET)
    if not form.is_valid():
        rtn = dict(
            errors=list(form.errors)
        )
        json = simplejson.dumps(rtn)
        return HttpResponseBadRequest(json, mimetype='text/plain')

    start = int(form.cleaned_data['start'] or 0)
    rows = int(form.cleaned_data['rows'] or 20)

    runs = Rundbruns.objects

    if form.cleaned_data['partition']:
        runs = runs.filter(partitionname__exact=form.cleaned_data['partition'])

    if form.cleaned_data['destination']:
        runs = runs.filter(destination__in=(form.cleaned_data['destination'],))

    if form.cleaned_data['endtime']:
        runs = runs.filter(starttime__lte=form.cleaned_data['endtime'])

    if form.cleaned_data['starttime']:
        runs = runs.filter(endtime__gte=form.cleaned_data['starttime'])


    count = runs.all().aggregate(Count('runid'))
    runs = runs.all().order_by('-runid')[start:rows]


    rtn = {
           'totalResults': count['runid__count'],
           'start': start,
           'runs': map(_api_run_as_json, runs)
    }
    return _api_response(request, rtn)

