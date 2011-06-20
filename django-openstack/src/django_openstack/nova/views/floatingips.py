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
Views for managing OpenStack Floating IPs.
"""

from django import http
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django_openstack.nova import exceptions
from django_openstack.nova import forms
from django_openstack.nova import shortcuts
from django_openstack.nova.exceptions import handle_nova_error

@login_required
@handle_nova_error
def index(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)
    floating_ips = project.get_floating_ips()
    associate_form = forms.AssociateFloatingIPForm(project)
    instance_id_display_dict = dict(associate_form.instance_choices)

    for floating_ip in floating_ips:
        floating_ip.floating_ip_id = floating_ip.public_ip.replace('.', '_')
        instance_id = floating_ip.instance_id.partition(' ')[0]
        floating_ip.instance_id_display = instance_id_display_dict.get(instance_id, floating_ip.instance_id)

    return render_to_response(
        'django_openstack/nova/floatingips/index.html', 
        {'associate_form': associate_form,
         'region': project.region,
         'project': project,
         'floating_ips': floating_ips}, 
        context_instance = template.RequestContext(request))

@login_required
@handle_nova_error
def allocate(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)

    try:
        floating_ip = project.allocate_floating_ip()
        messages.info(request, 'Floating IP %s allocated.' % floating_ip.public_ip)
    except exceptions.NovaApiError, e:
        messages.error(request, 'Unable to allocate IP: %s' % e.message)

    return redirect('nova_floatingips', project_id)

@login_required
@handle_nova_error
def release(request, project_id, floating_ip):
    project = shortcuts.get_project_or_404(request, project_id)

    try:
        success = project.release_floating_ip(floating_ip)
        if success:
            messages.info(request, 'Floating IP %s released.' % floating_ip)
        else:
            messages.error(request, 'Try again. Unable to release IP: %s' % floating_ip)
    except exceptions.NovaApiError, e:
        messages.error(request, 'Unable to release IP: %s' % e.message)

    return redirect('nova_floatingips', project_id)

@login_required
@handle_nova_error
def associate(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)

    if request.method == 'POST':
        form = forms.AssociateFloatingIPForm(project, request.POST)
        if form.is_valid():
            instance_id = form.cleaned_data['instance']
            floating_ip = form.cleaned_data['floating_ip']
            try:
                success = project.associate_floating_ip(instance_id, floating_ip)
                if success:
                    messages.info(request, 'Floating IP %s associated with %s.' % (floating_ip, instance_id))
                else:
                    messages.error(request, 'Try again. Unable to associate IP: %s' % floating_ip)
            except exceptions.NovaApiError, e:
                messages.error(request, 'Unable to associate Floating IP: %s' %  e.message)

    return redirect('nova_floatingips', project_id)

@login_required
@handle_nova_error
def disassociate(request, project_id, floating_ip):
    project = shortcuts.get_project_or_404(request, project_id)

    try:
        success = project.disassociate_floating_ip(floating_ip)
        if success:
            messages.info(request, 'Floating IP %s disassociated.' % floating_ip)
        else:
            messages.error(request, 'Try again. Unable to disassociate IP: %s' % floating_ip)
    except exceptions.NovaApiError, e:
        messages.error(request, 'Unable to disassociate IP: %s' % e.message)

    return redirect('nova_floatingips', project_id)

