from django.shortcuts import render, redirect
from .api import ApiZabbix
from django.http import JsonResponse, HttpResponse
from .forms import ReportForm
from .tables import MemberOfGroupTable
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django.utils import timezone
from zoneinfo import ZoneInfo
import os, json
from django.conf import settings

def index(request):
    ruta_json = os.path.join(settings.BASE_DIR, 'reports', 'custom-reports.json')
    with open(ruta_json, encoding='utf-8') as f:
        reportes = json.load(f)

    return render(request, "reports/index.html", {"reports": reportes})

def hgroup(request):
    """
    Render the index page for the report view.
    """
    api_zabbix = ApiZabbix()
    host_groups = api_zabbix.get_host_groups()
    list_host_groups = [(hg['groupid'], hg['name']) for hg in host_groups]
    
    if request.method == 'POST':        
        # Handle form submission if needed
        form = ReportForm(request.POST, hostgroups=list_host_groups)
    else:
        # Handle GET request, render the index page with host groups
        form = ReportForm(hostgroups=list_host_groups)

    if form.is_valid():
        # Process the form data
        groupid = form.cleaned_data['hostgroup']
        
        # Use the API to get the group information and hosts
        grupo = api_zabbix.get_host_group(groupid)
        info_hosts = api_zabbix.get_info_hosts(groupid)

        # Redirect or render a response after processing
        request.session['results'] = {
            'groupid': groupid,  # Store groupid in session for later use
            'member_of_group': info_hosts,  # Store the list of hosts in session
            'group_name': grupo['name'] if grupo else None,  # Store the group name in session
        }

        return redirect('getHosts')  # Redirect to the getHosts view
    else:
        # Render the index template with the context
        return render(request, 'reports/report-memberofgroup.html', {'form': form})

def getHosts(request):
    """
    Render the report page for the report view.
    """
    data = request.session.get('results', {})

    if data:
        groupid = data.get('groupid', None)
        hosts = data.get('member_of_group', [])
        group_name = data.get('group_name', None)
    else:
        groupid = None
        hosts = []
        group_name = None
    if not groupid:
        return redirect('index')
    
    query = request.GET.get('q', '').lower()

    if query:
        datos_filtrados = [
            row for row in hosts
            if query in str(row.get('hostid', '')).lower()
            or query in str(row.get('name', '')).lower()
            or query in str(row.get('status', '')).lower()
            or any(query in str(iface.get('ip', '')).lower() or query in str(iface.get('dns', '')).lower()
            for iface in row.get('interfaces', []))
        ]
    else:
        datos_filtrados = hosts

    tabla_hosts = MemberOfGroupTable(datos_filtrados)
    RequestConfig(request).configure(tabla_hosts)

    # Si es una petición HTMX, devolver solo el fragmento de la tabla
    if request.headers.get("HX-Request"):
        return render(request, "reports/table-results.html", {"table": tabla_hosts})

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, tabla_hosts)
        now = timezone.now()
        zone = ZoneInfo('America/La_Paz')  # Adjust the timezone as needed
        dt_local = now.astimezone(zone)
        if group_name:
            return exporter.response(f"Group-{group_name}-{dt_local.strftime('%Y%m%d-%H%M')}.{export_format}")
        else:
            return exporter.response(f"Group-Unknown-{dt_local.strftime('%Y%m%d-%H%M')}.{export_format}")

    return render(request, 'reports/member-of-group.html', {
        'table': tabla_hosts,
        'grupo': group_name,
        'query': query,
    })