# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Manage connections to Nova's admin API.
"""

import nova_adminclient as adminclient
from django.conf import settings


def get_nova_admin_connection(clc_url=None, region=None):
    """
    Returns a Nova administration connection.
    """
    return adminclient.NovaAdminClient(
        clc_url=clc_url or settings.NOVA_DEFAULT_ENDPOINT,
        region=region or settings.NOVA_DEFAULT_REGION,
        access_key=settings.NOVA_ACCESS_KEY,
        secret_key=settings.NOVA_SECRET_KEY)
