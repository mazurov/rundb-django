# Django settings for rundb_django project.
import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

configs = {
    '/home/mazurov/Projects/RunDb/rundb_django': 'production',
    '/opt/lampp/vhosts/rundb/rundb_django': 'production',
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Zurich'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.request",
  "django.core.context_processors.auth",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
#  "django.contrib.messages.context_processors.messages")
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'rundb_django.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or 
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
   ROOT_PATH + '/../rundb_templates',
#   '/usr/lib/pymodules/python2.6/debug_toolbar/template',
)

INSTALLED_APPS = (
     'rundb_django.rundb',
#     'debug_toolbar',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
#    'django.contrib.sites',
#     'django_extensions',
)

#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.cache.CacheDebugPanel',
#    'debug_toolbar.panels.logger.LoggingPanel',
#)

AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
)
# Import the configuration settings file - REPLACE projectname with your project
config_module = __import__('config.%s' % configs[ROOT_PATH], globals(), locals(), ['rundb_django'])

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)
