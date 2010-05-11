# This is an auto-generated Django model module.
# You'rundb_dev_admin.ll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field 
# names.
#
# Also note: You'rundb_dev_admin.ll have to insert the output of 
# 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.db.models import Sum, Count
from django.db import connection

from rundb_django import utils
import logging


class Rundbfills(models.Model):
    fill_id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    time_total = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    time_hvon = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    time_veloin = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    time_running = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    time_logged = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    lumi_total = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    lumi_hvon = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    lumi_veloin = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    lumi_running = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    lumi_logged = models.DecimalField(null=True, max_digits=32, decimal_places= -127, blank=True)
    
    @property
    def inefficiency(self):
        return round(100 * (1 - self.lumi_logged / self.lumi_total), 2)
    
    
    @property
    def delivered(self):
        return 100 - self.inefficiency
    
    @property
    def hvon_lost(self):
        return round(100 * (1 - self.lumi_hvon / self.lumi_total), 2)
    
    @property
    def veloin_lost(self):
        return round(100 * (1 - self.lumi_veloin / self.lumi_hvon), 2)
    
    @property
    def running_lost(self):    
        return round(100 * (1 - self.lumi_running / self.lumi_veloin), 2)
    
    @property
    def ontape_lost(self):    
        return round(100 * (1 - self.lumi_logged / self.lumi_running), 2)

    class Meta:
        db_table = u'rundbfills'

class Rundbdictnum(models.Model):
    type = models.CharField(unique=True, max_length=10)
    key = models.DecimalField(primary_key=True, unique=True, max_digits=0,
                                                          decimal_places= -127)
    value = models.CharField(max_length=512, blank=True)
    description = models.CharField(max_length=256, blank=True)
    class Meta:
        db_table = u'rundbdictnum'
        ordering = ['type']
        managed = False

class Rundbruns(models.Model):
    runid = models.IntegerField(unique=True, primary_key=True)
    fillid = models.IntegerField()
    partitionid = models.IntegerField()
    starttime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    startlumi = models.FloatField(null=True, blank=True)
    endlumi = models.FloatField(null=True, blank=True)
    _state = models.IntegerField(null=True, blank=True, db_column='state')
    beamenergy = models.FloatField(null=True, blank=True)
    runtype = models.CharField(max_length=255, blank=True)
    partitionname = models.CharField(max_length=16, blank=True)
    destination_old = models.IntegerField(null=True, blank=True)
    destination = models.CharField(max_length=16, blank=True)
    activity = models.CharField(max_length=512, blank=True)
    tck = models.CharField(max_length=512, blank=True)
    odin_trg_0 = models.IntegerField(null=True, blank=True)
    odin_trg_1 = models.IntegerField(null=True, blank=True)
    odin_trg_2 = models.IntegerField(null=True, blank=True)
    odin_trg_3 = models.IntegerField(null=True, blank=True)
    odin_trg_4 = models.IntegerField(null=True, blank=True)
    odin_trg_5 = models.IntegerField(null=True, blank=True)
    odin_trg_6 = models.IntegerField(null=True, blank=True)
    odin_trg_7 = models.IntegerField(null=True, blank=True)

    _all_subpartitions = []
    _all_partitions = []
    _all_runtypes = []
    _all_destinations = []
    _all_activities = []

    _states = ['', 'ACTIVE', 'ENDED', 'MIGRATING', 'NOT NEEDED', 'CREATED',
                                                                    'IN BKK'];
    _params = {}
    
    def __init__(self, *args, **kwargs): 
        super(Rundbruns, self).__init__(*args, **kwargs)
        self._file_counters = {}
                
    @classmethod
    def all_subpartitions(cls):
        if not Rundbruns._all_subpartitions:
            Rundbruns._all_subpartitions = list(
                    Rundbdictnum.objects.filter(type='DET').order_by('value'))
        return Rundbruns._all_subpartitions
    
    @classmethod
    def all_activities(cls):
        if not Rundbruns._all_activities:
            for item in Rundbruns.objects.values("activity").distinct().\
                                                    order_by("activity"):
                Rundbruns._all_activities.append(item['activity'])
        return Rundbruns._all_activities
    
    
    @classmethod
    def all_partitions(cls):
        if not Rundbruns._all_partitions:
            for item in Rundbruns.objects.values("partitionname").distinct().\
                                                    order_by("partitionname"):
                Rundbruns._all_partitions.append(item['partitionname'])
        return Rundbruns._all_partitions

    @classmethod
    def all_runtypes(cls):
        if not Rundbruns._all_runtypes:
            for runtype in Rundbruns.objects.values("runtype").distinct().\
                                                          order_by("runtype"):
                Rundbruns._all_runtypes.append(runtype['runtype'])
        return Rundbruns._all_runtypes
    
    @classmethod
    def all_destinations(cls):
        if not Rundbruns._all_destinations:
            for destination in Rundbruns.objects.values("destination").\
                                          distinct().order_by("destination"):
                Rundbruns._all_destinations.append(destination['destination'])
        return Rundbruns._all_destinations

    @property
    def subpartitions(self):
        for partition in Rundbruns.all_subpartitions():
            if 0 != (int(partition.key) & int(self.partitionid)):
                yield partition.value
    
    @property
    def subpartitions_count(self):
        return utils.bit_count(self.partitionid)

    @property
    def is_subpartitions_short(self):
        return self.subpartitions_count < 8
    
    @property
    def is_subpartitions_complete(self):
        return (0x7FFF ^ (self.partitionid & 0x7FFF)) == 0
    
    @property
    def xsubpartitions(self):
        xpartitions = 0x7FFF ^ (self.partitionid & 0x7FFF)
        for partition in Rundbruns.all_subpartitions():
            if 0 != (int(partition.key) & xpartitions):
                yield partition.value            

    @property
    def has_files(self):
        return self.rundbfiles_set.count() > 0
  
    @property
    def events(self):
        return self.rundbfiles_set.filter(stream='FULL').aggregate(
                            Sum('events')
                            )['events__sum']
    @property
    def file_counters(self):
        return Rundbruns.file_counters_stat(self)

    @classmethod
    def file_counters_stat(cls, runs):
        result = [[-10, 'EVENTS', 0, 'Number of events']]
        if not runs:
            return []
        args = []
        if not isinstance(runs, Rundbruns):
            (sql_clause, args) = runs._as_sql()
            cursor = connection.cursor();
            cursor.execute('SELECT SUM(events) FROM Rundbfiles'
                ' WHERE runid in (%s) AND stream=\'FULL\'' % sql_clause, args)
            (events,) = cursor.fetchone() 
            result[0][2] = events
            runs_clause = ' in (%s)' % sql_clause
        else:
            result[0][2] = runs.events
            runs_clause = '=%d' % runs.runid
        
        cursor = connection.cursor()
        cursor.execute('SELECT fc.type, d.value , SUM(fc.VALUE), d.description'
            ' FROM RUNDBFILECOUNTERS fc, RUNDBDICTNUM d, RUNDBFILES f WHERE'
            " fc.fileid=f.fileid AND d.key=fc.type and d.type='FCOUNT'"
            " AND f.runid %s AND f.stream='FULL'"
            " GROUP BY fc.type,d.value, d.description ORDER BY fc.TYPE" 
                % runs_clause, args)
        result += cursor.fetchall()
        return result

    @property
    def state(self):
        if self._state >= len(self._states):
            return ''
        return Rundbruns._states[self._state]
    @property
    def tck_hex(self):
        if  self.tck:
            return "0x%08X" % int(self.tck)
        return ""

    @property
    def params(self):
        if not self._params:
            for param in self.rundbrunparams_set.all():
                self._params[param.name] = param.value
        return self._params

    class Meta:
        db_table = u'rundbruns'
        managed = False

class Rundbrunparams(models.Model):
    run = models.ForeignKey(Rundbruns, db_column='runid', primary_key=True,
                                                                    unique=True)
    name = models.CharField(unique=True, max_length=32)
    value = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=32)
    class Meta:
        db_table = u'rundbrunparams'
        managed = False

class Rundbfiles(models.Model):
    fileid = models.IntegerField(unique=True, primary_key=True)
    run = models.ForeignKey(Rundbruns, db_column='runid')
    name = models.CharField(unique=True, max_length=255)
    stateid = models.IntegerField(db_column='state')
    bytes = models.IntegerField(null=True, blank=True)
    events = models.IntegerField(null=True, blank=True)
    stream = models.CharField(max_length=128, blank=True)
    creationtime = models.DateTimeField(null=True, blank=True)
    refcount = models.IntegerField(null=True, blank=True)
    timestamp = models.DateField(null=True, blank=True)
    refowner = models.CharField(max_length=32, blank=True)
    refdate = models.DateField(null=True, blank=True, auto_now=True)

    _all_states = None
    _state = None
    _params = None

    def state(self):
        if not self._state:
            for state in Rundbfiles.all_states():
                if state.key == self.stateid:
                    self._state = state.value
      
        if not self._state:
            self._state = 'UNDEFINED'
        return self._state

    def physstat(self):
        return self.param("physstat")
    
    def directory(self):
        return self.param("directory")


    def param(self, name):
        for param in self.rundbfileparams_set.all():
            if param.name == name:
                return  param.value
        return None

    def castor(self):
        if self.run.destination == 'OFFLINE' and self.directory():
            return self.directory().replace('/daqarea',
                                    '/castor/cern.ch/grid') + "/" + self.name
        return None

    def has_nevents(self):
        for i in range(8):
            if getattr(self, 'nevent_%i' % i):
                return True
        return False
    
    def pin(self, user):
        if self.refcount == 0:
            self.refcount = 1
            self.refowner = user.username
        else:
            self.refcount = 0
            self.refowner = ''
        log = Rundbdatamover()
        log.pin(self.name, user.username, self.refcount)
        log.save()

    def log(self):
        return Rundbdatamover.objects.filter(id=self.name).order_by('-time')
    
    def shortlog(self):
        return self.log()[0:10]

    @property
    def file_counters(self):
        result = []
        for counter in self.rundbfilecounters_set.all():
            result.append((counter.type, counter.counter.key, counter.value,
                                                counter.counter.description))
        return result
    @classmethod
    def all_states(cls):
        if None == Rundbfiles._all_states:
            Rundbfiles._all_states = list(
                Rundbdictnum.objects.filter(type='FSTATE').order_by('value'))
        return Rundbfiles._all_states

    class Meta:
        db_table = u'rundbfiles'
        managed = False

class Rundbfilecounters(models.Model):
    file = models.ForeignKey(Rundbfiles, db_column='fileid', primary_key=True,
                                                                    unique=True)
    type = models.IntegerField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    _counter = None
    
    @property
    def counter(self):
        if not self._counter:
            self._counter = Rundbdictnum.objects.filter(type='FCOUNT').filter(
                                                        key=self.type).all()[0]
        return self._counter
      
    class Meta:
        ordering = ['type']
        db_table = u'rundbfilecounters'

class Rundbfileparams(models.Model):
    file = models.ForeignKey(Rundbfiles, db_column='fileid', primary_key=True,
                                                                    unique=True)
    name = models.CharField(unique=True, max_length=32)
    value = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=32)
    class Meta:
        db_table = u'rundbfileparams'
        managed = False

class Rundbdatamover(models.Model):
    id = models.CharField(max_length=50, blank=True, unique=True)
    type = models.CharField(max_length=10, blank=True, unique=True)
    time = models.DateTimeField(null=True, blank=True, auto_now=True,
                                                            primary_key=True)
    message = models.CharField(max_length=255, blank=True)
    trials = models.IntegerField(null=True, blank=True)
    
    def file(self):
        return Rundbfiles.objects.get(name=self.id)
    
    def pin(self, filename, username, refcount):
        self.id = filename
        self.type = "pin"
        self.message = username + ": "
        if refcount == 0:
            self.message += "UNPINED"
        else:
            self.message += "PINNED"
    
    class Meta:
        db_table = u'rundbdatamover'
        managed = False
        ordering = ['-time']
        
