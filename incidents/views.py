from django.shortcuts import render
from django.http import HttpResponse
from .tables import IncidentsOpenTable,MasivosNewTable,IncidentsClosedTable
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
import requests, json, pytz
from django.http import JsonResponse
from datetime import datetime, timedelta
#from subprocess import getoutput as ejec

def _change_to_local_hour(date_other):
    dt = datetime.strptime(date_other, "%Y-%m-%d %H:%M:%S")
    return dt + timedelta(hours=2)

def _strtodate(date: str) -> str:
    date_start = datetime.strptime(date+' -04:00','%Y-%m-%d %H:%M:%S %z')
    aux_dt =  datetime.now(pytz.timezone('America/La_Paz')) 
    aux_dt = aux_dt - date_start
    if (aux_dt.days == 0):
        if (aux_dt.seconds//3600 == 0):
            return f'{(aux_dt.seconds//60)%60}m'
        else:
            return f'{aux_dt.seconds//3600}h {(aux_dt.seconds//60)%60}m'
    else:
        return f'{aux_dt.days}d {aux_dt.seconds//3600}h {(aux_dt.seconds//60)%60}m'

def _get_request(estado, fecha_ini, fecha_fin):
    url = f'https://itsmtigo.service-now.com/api/tcdps/excelreportebolivia_inc?state={estado}&start_opened_at={fecha_ini}&end_opened_at={fecha_fin}'
    proxies = {
#            'http': 'http://webproxy.tigo.net.bo:8080',
#            'https': 'http://webproxy.tigo.net.bo:8080',
            }
    resp = requests.get(url, proxies=proxies)
    if resp.status_code != 200:
        return HttpResponse('ERROR GET ' + url + f' {resp.status_code}')
    #ejec(f'echo "{url}" >> /tmp/incidentes.log')
    return resp

def _filtrar_tabla_cerrados(tipo, fecha_ini, fecha_fin=f'{datetime.now(pytz.timezone("America/La_Paz"))}'):

    d = datetime.now(pytz.timezone("America/La_Paz"))
    fecha_fin = d.strftime("%Y-%m-%d")
    resp = _get_request(tipo, fecha_ini, fecha_fin)
    data = resp.json()['result']['incidents']    

    #add data within space in key
    for i in range(len(data)):
        data[i]['Service_Offerings'] = ", ".join(data[i]['Service Offerings'])
        data[i]['Impacted_Services'] = ", ".join(data[i]['Impacted Services'])
        data[i]["Affected_CIs"] = ", ".join(data[i]["Affected CIs"])
        dt_local = _change_to_local_hour(data[i]["u_issue_start_date"])
        data[i]["u_issue_start_date"] = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        if data[i]["state"].lower() != 'cancelado': 
            dt_local = _change_to_local_hour(data[i]["u_issue_end_date"])
            data[i]["u_issue_end_date"] = dt_local.strftime("%Y-%m-%d %H:%M:%S")

    #filter lists dicts
    return [
            i for i in data if "bolivia" in i["u_country"].lower() and
            i["category"].lower() != "digital" and
            i["priority"].lower() != '4 - baja' and
            "_BO" in i["assignment_group"].strip() or
            i["assignment_group"].strip() == "" and
            i["caller_id"].lower() != 'noc app-core' and
            "_BO" in i["Impacted_Services"].strip()
            ]

def _filtrar_tabla_masivos(tipo, fecha_ini, fecha_fin=f'{datetime.now(pytz.timezone("America/La_Paz"))}'):

    d = datetime.now(pytz.timezone("America/La_Paz"))
    fecha_fin = d.strftime("%Y-%m-%d")
    resp = _get_request(tipo, fecha_ini, fecha_fin)
    data = resp.json()['result']['incidents']    

    #add data within space in key
    for i in range(len(data)):
        data[i]['Impacted_Services'] = ", ".join(data[i]['Impacted Services'])
        dt_local = _change_to_local_hour(data[i]["u_issue_start_date"])
        data[i]["u_issue_start_date"] = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        data[i]['description'] = data[i]['description'].replace('{','')
        data[i]['description'] = data[i]['description'].replace('}','')
        data[i]['time_acum'] = _strtodate(data[i]["u_issue_start_date"])

    #filter lists dicts
    return [
            i for i in data if i["assigned_to"] != '' and 
            "bolivia" in i["u_country"].lower() and
            i["category"].lower() != "digital" and
            i["assignment_group"].strip() == "" and
            i["caller_id"].lower() != "temip uca" and
            #i["caller_id"].lower() == 'call center bo' and
            i["assigned_to"].strip() == '' and
            ("_BO" in i["Impacted_Services"].strip() or
            i["Impacted_Services"].strip() == '')
            ]

def _filtrar_tabla_open(tipo, fecha_ini, fecha_fin=f'{datetime.now(pytz.timezone("America/La_Paz"))}'):

    d = datetime.now(pytz.timezone("America/La_Paz"))
    fecha_fin = d.strftime("%Y-%m-%d")
    resp = _get_request(tipo, fecha_ini, fecha_fin)
    data = resp.json()['result']['incidents']    

    #add data within space in key
    for i in range(len(data)):
        data[i]['Service_Offerings'] = ", ".join(data[i]['Service Offerings'])
        data[i]['Impacted_Services'] = ", ".join(data[i]['Impacted Services'])
        data[i]["Affected_CIs"] = ", ".join(data[i]["Affected CIs"])
        dt_local = _change_to_local_hour(data[i]["u_issue_start_date"])
        data[i]["u_issue_start_date"] = dt_local.strftime("%Y-%m-%d %H:%M:%S")


    #filter lists dicts
    return [
            i for i in data if "bolivia" in i["u_country"].lower() and
            i["category"].lower() != "digital" and
            i["priority"].lower() != '4 - baja' and
            ("_BO" in i["assignment_group"] or
            i["assignment_group"].strip() == "") and
            ("_BO" in i["Impacted_Services"] or
            i["Impacted_Services"].strip() == '') and
            i["caller_id"].lower() != 'noc app-core'
            ]

def _filtrar_tabla_oym(tipo, fecha_fin=f'{datetime.now(pytz.timezone("America/La_Paz"))}'):

    d = datetime.now(pytz.timezone("America/La_Paz"))
    dt_fin = d - timedelta(days=3)
    resp = _get_request(tipo, dt_fin.strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d"))
    data = resp.json()['result']['incidents']    

    #add data within space in key
    for i in range(len(data)):
        data[i]['Service_Offerings'] = ", ".join(data[i]['Service Offerings'])
        data[i]['Impacted_Services'] = ", ".join(data[i]['Impacted Services'])
        data[i]["Affected_CIs"] = ", ".join(data[i]["Affected CIs"])
        dt_local = _change_to_local_hour(data[i]["u_issue_start_date"])
        data[i]["u_issue_start_date"] = dt_local.strftime("%Y-%m-%d %H:%M:%S")
        data[i]['description'] = data[i]['description'].replace('{','')
        data[i]['description'] = data[i]['description'].replace('}','')
        data[i]['time_acum'] = _strtodate(data[i]["u_issue_start_date"])

    #filter lists dicts
    lista_ti = [
            i for i in data 
            if i["assigned_to"] != '' and 
            "bolivia" in i["u_country"].lower() and
            i["category"].lower() != "digital" and
            i["category"].lower() == 'ti' and
            i["priority"].lower() != '4 - baja' and
            ("_BO" in i["assignment_group"] or
            i["assignment_group"].strip() == "") and
            ("_BO" in i["Impacted_Services"] or
            i["Impacted_Services"].strip() == '') and
            i["caller_id"].lower() != 'noc app-core'
            ]

    lista_mobile = [
            i for i in data 
            if i["assigned_to"] != '' and 
            "bolivia" in i["u_country"].lower() and
            i["category"].lower() != "digital" and
            i["category"].lower() == 'móvil' and
            i["priority"].lower() != '4 - baja' and
            ("_BO" in i["assignment_group"] or
            i["assignment_group"].strip() == "") and
            ("_BO" in i["Impacted_Services"] or
            i["Impacted_Services"].strip() == '') and
            i["caller_id"].lower() != 'noc app-core'
            ]

    lista_fijo = [
            i for i in data 
            if i["assigned_to"] != '' and 
            "bolivia" in i["u_country"].lower() and
            i["category"].lower() != "digital" and
            i["category"].lower() == 'fijo' and
            i["priority"].lower() != '4 - baja' and
            ("_BO" in i["assignment_group"] or
            i["assignment_group"].strip() == "") and
            ("_BO" in i["Impacted_Services"] or
            i["Impacted_Services"].strip() == '') and
            i["caller_id"].lower() != 'noc app-core'
            ]

    return [lista_fijo, lista_ti, lista_mobile]

def servicenow(request):

    if request.method == 'POST':
        return HttpResponse('ERROR AL USAR METODO POST')
    fecha_inicio = request.GET.get('inicio',None)
    tz = pytz.timezone('America/La_Paz')
    fecha_actual = datetime.now(tz)

    if fecha_inicio == None:
        fecha_inicio = fecha_actual - timedelta(days=3)
    elif fecha_inicio == '':
        return HttpResponse('ERROR seleccione fecha antes de aplicar el rango')
    elif isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_hace_tres_dias = fecha_actual - timedelta(days=3)

##Masivos new
    data_masivos = _filtrar_tabla_masivos(1,fecha_inicio.strftime("%Y-%m-%d"))
    tabla_masivos = MasivosNewTable(data_masivos)
    RequestConfig(request, paginate={"per_page": 10}).configure(tabla_masivos)
    export_format = request.GET.get("_new_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, tabla_masivos)
        return exporter.response(f"incidentes_masivos_{fecha_actual.strftime('%Y%m%d')}.{export_format}")
   
##OPEN  
    data_open = _filtrar_tabla_open(2, fecha_inicio.strftime("%Y-%m-%d"))
    table_open = IncidentsOpenTable(data_open)
    RequestConfig(request, paginate={"per_page": 10}).configure(table_open)
    export_format = request.GET.get("_open_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table_open)
        return exporter.response(f"incidentes_abiertos_{fecha_actual.strftime('%Y%m%d')}.{export_format}")
    
##Resolved - closed, canceled
    data_resolved = _filtrar_tabla_cerrados(6,fecha_hace_tres_dias.strftime("%Y-%m-%d"))
    data_closed = _filtrar_tabla_cerrados(7,fecha_hace_tres_dias.strftime("%Y-%m-%d"))
    data_canceled = _filtrar_tabla_cerrados(8,fecha_hace_tres_dias.strftime("%Y-%m-%d"))

    data_final = data_resolved + data_closed + data_canceled
    table_closed = IncidentsClosedTable(data_final)
    RequestConfig(request, paginate={"per_page": 10}).configure(table_closed)
    export_format = request.GET.get("_close_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table_closed)
        return exporter.response(f"incidentes_resueltos_{fecha_actual.strftime('%Y%m%d')}.{export_format}")


    return render(request, "incidents/index.html", {
                        "new": tabla_masivos,
                        "open": table_open,
                        "close": table_closed,
                        "fecha_update": fecha_actual.strftime('%Y-%m-%d %H:%M:%S'),
                                            })

def index(request):
    if request.method == 'POST':
        return HttpResponse('ERROR AL USAR METODO POST')
    tz = pytz.timezone('America/La_Paz')
    fecha_actual = datetime.now(tz)

##Masivos  
    data_masivos = _filtrar_tabla_masivos(1,fecha_actual.strftime("%Y-%m-%d"))
    tabla_masivos = MasivosNewTable(data_masivos)
    RequestConfig(request, paginate={"per_page": 10}).configure(tabla_masivos)

#Fijo,IT,Mobile
    data_fijo, data_it, data_mobile = _filtrar_tabla_oym(2)
    tabla_fijo = IncidentsOpenTable(data_fijo)
    RequestConfig(request, paginate={"per_page": 10}).configure(tabla_fijo)
    tabla_it = IncidentsOpenTable(data_it)
    RequestConfig(request, paginate={"per_page": 10}).configure(tabla_it)
    tabla_mobile = IncidentsOpenTable(data_mobile)
    RequestConfig(request, paginate={"per_page": 10}).configure(tabla_mobile)

    return render(request, "incidents/oym.html", {
                        "diagnostico": tabla_masivos,
                        "fijo": tabla_fijo,
                        "it": tabla_it,
                        "mobile": tabla_mobile,
                        "fecha_update": fecha_actual.strftime('%Y-%m-%d %H:%M:%S %:z'),
                                            })


