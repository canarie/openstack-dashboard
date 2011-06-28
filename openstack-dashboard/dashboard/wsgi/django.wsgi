import site
site.addsitedir('/usr/local/openstack-dashboard/dair/openstack-dashboard/.dashboard-venv/lib/python2.6/site-packages')

import logging
import os
import sys
import django.core.handlers.wsgi
from django.conf import settings

path = '/usr/local/openstack-dashboard/dair/openstack-dashboard'
if path not in sys.path:
    sys.path.append(path)

path = '/usr/local/openstack-dashboard/dair/django-openstack/src'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
sys.stdout = sys.stderr

DEBUG = False

application = django.core.handlers.wsgi.WSGIHandler()

