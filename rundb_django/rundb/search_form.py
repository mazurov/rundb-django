from django import forms
from django.forms.extras import SelectDateWidget
from rundb_django.rundb.models import Rundbruns

class SearchForm(forms.Form):
  runid         = forms.IntegerField(min_value=1,required=False)
  partitions    = forms.MultipleChoiceField(required=False)
  runtypes      = forms.MultipleChoiceField(required=False)
  destinations  = forms.MultipleChoiceField(required=False)
  runid_min     = forms.IntegerField(min_value=0,required=False)
  runid_max     = forms.IntegerField(min_value=0,required=False)
  startdate     = forms.DateTimeField(('%d.%m.%Y',),widget=forms.DateTimeInput(format='%d.%m.%Y'),required=False)
  enddate       = forms.DateTimeField(('%d.%m.%Y',),widget=forms.DateTimeInput(format='%d.%m.%Y'),required=False)
  starttime     = forms.TimeField(required=False)
  endtime       = forms.TimeField(required=False)
  onpage        = forms.ChoiceField(choices=[(10,10),(50,50),(100,100),
                                                        (200,200)],initial=10)

  def __init__(self, partitions, runtypes,destinations,*args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    self.fields['partitions'].choices = partitions
    self.fields['runtypes'].choices = runtypes
    self.fields['destinations'].choices = destinations
      
    self.fields['partitions'].widget.attrs['class'] = 'span-5'
    self.fields['runtypes'].widget.attrs['class'] = 'span-5'
    self.fields['destinations'].widget.attrs['class'] = 'span-5'
    
    self.fields['startdate'].widget.attrs['title'] = 'yyyy-mm-dd'
    self.fields['starttime'].widget.attrs['title'] = 'hh:mm'
    self.fields['enddate'].widget.attrs['title'] = 'yyyy-mm-dd'
    self.fields['endtime'].widget.attrs['title'] = 'hh:mm'
    
