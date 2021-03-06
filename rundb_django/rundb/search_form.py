from django import forms
from django.forms.widgets import RadioSelect
import logging
import pprint
class SearchForm(forms.Form):
    partitions = forms.ChoiceField(required=False, choices=())
    runtypes = forms.ChoiceField(required=False, choices=())
    destinations = forms.ChoiceField(required=False, choices=())
    activities = forms.ChoiceField(required=False, choices=())
    velo_position = forms.ChoiceField(choices=(('', 'ANY'), ('OPEN', 'OPEN'),
                            ('Closed', 'CLOSED')), required=False)
    magnet_state = forms.ChoiceField(required=False, choices=(('', 'ANY'),
                            ('OFF', 'OFF'), ('UP', 'UP'), ('DOWN', 'DOWN')))
    beamenergy = forms.FloatField(required=False)    
    runid_min = forms.IntegerField(min_value=0, required=False)
    runid_max = forms.IntegerField(min_value=0, required=False)
    fillid_min = forms.IntegerField(min_value=0, required=False)
    fillid_max = forms.IntegerField(min_value=0, required=False)
    startdate = forms.DateTimeField(('%d.%m.%Y',),
                widget=forms.DateTimeInput(format='%d.%m.%Y'), required=False)
    enddate = forms.DateTimeField(('%d.%m.%Y',),
                widget=forms.DateTimeInput(format='%d.%m.%Y'), required=False)
    starttime = forms.TimeField(required=False)
    endtime = forms.TimeField(required=False)
    pinned = forms.TypedChoiceField(widget=RadioSelect, required=False,
                                                        coerce=int, initial=0)
    pinned_all = forms.BooleanField(label='Run contains any pinned files',
                                                                required=False)
    pinned_user = forms.BooleanField(label='Run contains files pinned by user',
                                                                required=False)
    onpage = forms.ChoiceField(choices=((10, 10), (50, 50), (100, 100),
                                                (200, 200),), initial='10')
    is_show_stat = forms.BooleanField(label='Show statistic', required=False,
                                                                   initial=True)

    def __init__(self, user, partitions, runtypes, destinations, activities,
                  data):
        if data:
          super(SearchForm, self).__init__(data)
        else:
          super(SearchForm, self).__init__()
        self.initial = {'partitions':'LHCb'}
        self.fields['partitions'].choices = partitions
        self.fields['partitions'].initial = 'LHCb'
        self.fields['destinations'].choices = destinations
        self.fields['destinations'].initial = 'OFFLINE'
        self.fields['runtypes'].choices = runtypes
        self.fields['activities'].choices = activities

        pinned = []
        pinned.append((0, 'Do not check'))
        pinned.append((1, 'Run contains pinned files'))
        if user.is_authenticated():
            pinned.append((2,
                    "Run contains  files pinned by user %s" % user.username))
    
        self.fields['pinned'].choices = pinned
        self.fields['partitions'].widget.attrs['class'] = 'span-5'
        self.fields['runtypes'].widget.attrs['class'] = 'span-5'
        self.fields['destinations'].widget.attrs['class'] = 'span-5'
        self.fields['activities'].widget.attrs['class'] = 'span-5'
        #self.fields['partitions'].widget.attrs['style'] = 'height:200px'
        #self.fields['runtypes'].widget.attrs['style'] = 'height:200px'
        #self.fields['destinations'].widget.attrs['style'] = 'height:200px'
        #self.fields['activities'].widget.attrs['style'] = 'height:200px'
    
        self.fields['startdate'].widget.attrs['title'] = 'dd.mm.yyyy'
        self.fields['starttime'].widget.attrs['title'] = 'hh:mm'
        self.fields['enddate'].widget.attrs['title'] = 'dd.mm.yyyy'
        self.fields['endtime'].widget.attrs['title'] = 'hh:mm'



class ApiForm(forms.Form):
    """
    The form used for the query arguments of the api_search view.
    """
    rows = forms.IntegerField(min_value=1, required=False)
    start = forms.IntegerField(min_value=0, required=False)

    partition = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    starttime = forms.DateTimeField(('%Y-%m-%dT%H:%M:%S',), required=False)
    endtime = forms.DateTimeField(('%Y-%m-%dT%H:%M:%S',), required=False)
    
