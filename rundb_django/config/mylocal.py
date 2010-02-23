ADMINS = (
    ('Vasya Pupkin', 'vasya@pupkin.com'),
)
MANAGERS = ADMINS

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ( '127.0.0.1' )



# Make this unique, and don't share it with anybody.
SECRET_KEY = ')&&k=e8jw5e+gzy5w))^rtg9)&&k=e8jw5e+gzy5w))^rtg9'

# Database configuration
DATABASE_ENGINE = 'sqllite'
DATABASE_NAME = ''       # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = '' # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '' # Set to empty string for default. Not used with sqlite3.


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or 
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
   '/home/vasya/Projects/site/templates',
#   '/usr/lib/pymodules/python2.6/debug_toolbar/template',
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/vasya/Projects/site/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
