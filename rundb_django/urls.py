from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^rundb_django/', include('rundb_django.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$','django.views.static.serve',
              {'document_root': '/home/mazurov/Projects/rundb/rundb_media'}),
    (r'^login$','django.contrib.auth.views.login', 
                                  {'template_name': 'lhcb/lhcb_login.html','redirect_field_name':'next_page'}),
    (r'^logout$','django.contrib.auth.views.logout',{'redirect_field_name':'next_page'}),    
    
    (r'^$',"rundb_django.rundb.views.index"),
    (r'^rundb/$',"rundb_django.rundb.views.redirect"),
    
    (r'^rundb/run$',"rundb_django.rundb.views.run"),
    (r'^rundb/maintable$',"rundb_django.rundb.views.maintable"),
    (r'^rundb/file$',"rundb_django.rundb.views.file"),
    (r'^rundb/files$',"rundb_django.rundb.views.files"),
    (r'^rundb/file-pin$',"rundb_django.rundb.views.file_pin"),
    (r'^rundb/file-log$',"rundb_django.rundb.views.file_log"),

    (r'^api/run/(?P<runid>\d+)/$', 'rundb_django.rundb.views.api_run'),
    (r'^api/search/$', 'rundb_django.rundb.views.api_search'),

)
