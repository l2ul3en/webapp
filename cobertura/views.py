from django.shortcuts import render
from django.http import HttpResponse
from .models import Node
from .tables import NodeTable, CoverageTable
from django_tables2 import SingleTableView, RequestConfig
from django_tables2.export.export import TableExport
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from zoneinfo import ZoneInfo

@login_required
def index(request):
    if request.method == 'POST':
        nodo = request.POST.get('text_nodo', 'None')
    else:
        nodo = request.GET.get('text_nodo', 'None')

    now = timezone.now()
    zone = ZoneInfo('America/Caracas')
    dt_local = now.astimezone(zone)
    query = Node.objects.filter(name__iregex=nodo)
    table = CoverageTable(query)
    RequestConfig(request).configure(table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"Nodos-{dt_local.strftime('%Y%m%d-%H%M')}.{export_format}")

    return render(request, "cobertura/index.html", {
                "table": table
                    })
