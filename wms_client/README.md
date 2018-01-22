
WMS Web Client Template
======

**Create a Web Interface to a MOCA application server with Django!**


Introduction
____________

This template is an example of creating a web interface that connects to a MOCA application server.  The login functionality
allows you to authenticate using your MOCA application credentials.  Once authenticated, you can then create custom web
screens that can run MOCA commands and retrieve the results back.

The Home page has a few examples of custom dashboard widgets as a reference for your own custom web project.


Setup
____________

Assuming you already have a working knowledge of Django project setup, do the following to get this example up and running:

1) Create your virtual environment, activate it, and install the required packages in the requirements.txt file
2) Start a new Django project/perform any migrations/create superuser, etc.
2) Add the 'home' app to your project and register it in settings.py
3) Copy the static, templates directories to your project
4) Copy the backends.py file to your project
5) Modify the base urls.py file to match the examples
6) Modify settings.py as follows:

  ALLOWED_HOSTS = ['localhost']  #for use on your local machine

  TEMPLATES-->DIRS section: [os.path.join(BASE_DIR, 'wms_client/templates')]

  TEMPLATES-->OPTIONS context_processors section: Add 'django.template.context_processors.request',

  AUTHENTICATION_BACKENDS = ['wms_client.backends.MocaBackend', 'django.contrib.auth.backends.ModelBackend']

  SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

  SESSION_EXPIRE_AT_BROWSER_CLOSE = True

  MOCA_URL = '<your MOCA URL address goes here'

  WH_ID = '<your warehouse id to login goes here>'

  STATIC_URL = '/static/'

  STATICFILES_DIRS = [
      os.path.join(BASE_DIR, 'wms_client/static'),
  ]
  
