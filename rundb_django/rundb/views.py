import datetime
from django.template import RequestContext,loader
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from rundb_django.rundb.models import Rundbruns,Rundbfiles
from rundb_django.rundb.search_form import SearchForm



def search_form(request=None):
  partitions = []
  for partition in Rundbruns.all_partitions():
    partitions.append((partition,partition))
    
  runtypes = []
  for runtype in Rundbruns.all_runtypes():
    runtypes.append((runtype,runtype))
  
  destinations = []
  for destination in Rundbruns.all_destinations():
    destinations.append((destination,destination))
  
  activities = []
  for activity in Rundbruns.all_activities():
    destinations.append((activity,activity))
  
  return SearchForm(request.user,partitions,runtypes,destinations,activities,request.REQUEST) 
  

def index(request):
    return render_to_response('rundb/rundb_index.html',
      {'form':search_form(request)},context_instance=RequestContext(request))

def redirect(request):
  return HttpResponseRedirect("/")

"""
Result for ajax form
"""
def maintable(request):
  form = search_form(request)

  if form.is_valid():
    runs = Rundbruns.objects   

    if form.cleaned_data['runid']:
      runs = runs.filter(runid=form.cleaned_data['runid'])
    else:
      if form.cleaned_data['runid_min']:
        runs = runs.filter(runid__gte=form.cleaned_data['runid_min'])
      if form.cleaned_data['runid_max']:
        runs = runs.filter(runid__lte=form.cleaned_data['runid_max'])
      if form.cleaned_data['partitions']:
        runs = runs.filter(partitionname__in=form.cleaned_data['partitions'])
      if form.cleaned_data['runtypes']:
        runs = runs.filter(runtype__in=form.cleaned_data['runtypes'])
      if form.cleaned_data['destinations']:
        runs = runs.filter(destination__in=form.cleaned_data['destinations'])
      if form.cleaned_data['activities']:
        runs = runs.filter(activity__in=form.cleaned_data['activities'])
      
      if form.cleaned_data['pinned'] == 1:
        runs = runs.filter(rundbfiles__refcount__gt=0)
      
      if (request.user.is_authenticated()) and (form.cleaned_data['pinned'] == "2"):
        runs = runs.filter(rundbfiles__refowner=request.user.username)

      
      if form.cleaned_data['startdate']:
        starttime = datetime.datetime.combine(form.cleaned_data['startdate'],datetime.time.min)
        if form.cleaned_data['starttime']:
          starttime = datetime.datetime.combine(starttime,form.cleaned_data['starttime'])
        runs = runs.filter(starttime__gte=starttime)
      else:
        if form.cleaned_data['starttime']:
          starttime = datetime.combine(datetime.now(), form.cleaned_data['starttime'])
          runs = runs.filter(starttime__gte=starttime)
      
      if form.cleaned_data['enddate']:
        endtime = datetime.datetime.combine(form.cleaned_data['enddate'],datetime.time.max)
        if form.cleaned_data['endtime']:
          endtime = datetime.datetime.combine(endtime,form.cleaned_data['endtime'])
        runs = runs.filter(endtime__lte=endtime)
      else:
        if form.cleaned_data['endtime']:
          endtime = datetime.combine(datetime.now(),form.cleaned_data['endtime'])
          runs = runs.filter(endtime__gte=endtime)

    tpl = loader.get_template('rundb/rundb_maintable.html')
    ctx = RequestContext(request,
      {'runs': runs.all().order_by('-runid')[0:form.cleaned_data['onpage']]})
    json = simplejson.dumps(tpl.render(ctx))
  else:
    json = simplejson.dumps("form not valid"+str(form.errors))

  return HttpResponse(json, mimetype='application/json')


def files(request):
  #--------------------------------------------------------------------------------------
  if 'p' in request.GET:
    page = int(request.GET['p'])
  else:
    page = 1
  #--------------------------------------------------------------------------------------
  onpage=10
  #--------------------------------------------------------------------------------------
  if page==1:
    tplfile = 'rundb/rundb_files.html'
  else:
    tplfile = 'rundb/rundb_files_rows.inc.html'
  #--------------------------------------------------------------------------------------
  tpl = loader.get_template(tplfile)
  run = Rundbruns.objects.get(runid=request.GET['runid']);
  #--------------------------------------------------------------------------------------
  # Context
  #--------------------------------------------------------------------------------------
  context = {'run':run,'files': run.rundbfiles_set.all()[(page-1)*onpage:page*onpage]}
  if run.rundbfiles_set.count() > page*onpage:
    context['next'] = page+1
  #--------------------------------------------------------------------------------------
  ctx = RequestContext(request,context)
  #--------------------------------------------------------------------------------------
  return HttpResponse(simplejson.dumps(tpl.render(ctx)),
                                                mimetype='application/json');

@login_required
def file_pin(request):
  file = Rundbfiles.objects.get(fileid=request.GET['fileid'])
  file.pin(request.user)
  file.save();
  result = simplejson.dumps({'refcount':file.refcount})
  return HttpResponse(result,mimetype='application/json')

def file_log(request):
  file = Rundbfiles.objects.get(fileid=request.GET['fileid'])
  return render_to_response('rundb/rundb_file_log.html',
      {'file':file},context_instance=RequestContext(request))

def run(request):
  run = Rundbruns.objects.get(runid=request.GET['runid'])
  odins = []
  for i in range(7):
    odins.append(getattr(run,'odin_trg_'+str(i)))

  return render_to_response('rundb/rundb_run.html',
      {'single':True, 'run':run,'runs':[run],'iodins':range(7),'odins':odins},context_instance=RequestContext(request))

def file(request):
  file = Rundbfiles.objects.get(fileid=request.GET['fileid'])
  run = file.run
  return render_to_response('rundb/rundb_file.html',
      {'single':True, 'file':file,'files':[file],'run':run},context_instance=RequestContext(request))
