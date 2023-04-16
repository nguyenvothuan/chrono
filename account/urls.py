#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.urls import path

# Rest Framework imports.

# Third Party Library imports

# local imports.
from account.views import Punch, GetStartTime

app_name = 'accounts'

urlpatterns = [
    path('punch', Punch.as_view(), name='punch in punch out'), 
    path('punch-in-time', GetStartTime.as_view(), name = "get punch in time")
]
