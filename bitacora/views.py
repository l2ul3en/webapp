from django.shortcuts import render
from .models import City, Electric, Cmts, Node, Source
from django.http import HttpResponse
from django.contrib import messages


def index(request):
    COLUMNS = ['CMTS', 'IP', 'NODO', 'IP', 'MAC', 'US', 'DS', 'FUENTE', 'IP', 'MAC', 'US', 'DS', 'CODIGO', 'ELECTRICA', 'TELEFONO']
    #COLUMNS = ['FUENTE', 'FIP', 'FMAC', 'FUS', 'FDS', 'CODIGO', 'GRAFICA']
    
    if request.method == 'POST':
        nodo = request.POST.get('text_nodo', 'None')
    else:
        nodo = request.GET.get('text_nodo', 'None')
    
    q1 = Source.objects.filter(name__iregex=nodo).select_related("cmts", "electric")
    q2 = Node.objects.filter(name__iregex=nodo).select_related("cmts")
    rows = list()
    if q1.exists() and q2.exists():
        messages.success(request, "Busqueda exitosa.!!")
        for i in range(len(q1)):
            rows.append({'cmts': q1[i].cmts.name,
                    'address': q1[i].cmts.ip,
                    'nodo': q2[i].name,
                    'ip': q2[i].ip,
                    'mac': q2[i].mac,
                    'us': q2[i].upstream,
                    'ds': q2[i].downstream,
                    'fuente': q1[i].name,
                    'fip': q1[i].ip,
                    'fmac': q1[i].mac,
                    'fus': q1[i].upstream, 
                    'fds': q1[i].downstream, 
                    'code': q1[i].service_code, 
                    'fgraph': q1[i].graph, 
                    'graph': q2[i].graph,
                    'electric': q1[i].electric.name,
                    'telephone': q1[i].electric.telephone,
                    })
    data={'data':rows, 'columnas':COLUMNS}
    #return HttpResponse("")
    return render(request, 'bitacora/index.html', data)
