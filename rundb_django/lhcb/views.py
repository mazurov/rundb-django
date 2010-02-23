from django.template import Context, RequestContext,loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import logout

from rundb_django.lhcb.forms import LoginForm

def login_view(request):
    if request.method == "POST":    
        loginform = LoginForm(request.POST)
        if loginform.login(request):            
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/login?error")
    else:   
        loginform = LoginForm()    
        form = LoginForm()
        return render_to_response('login.html',
                {'form':form},context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")