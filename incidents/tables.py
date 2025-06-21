import django_tables2 as tables
from utils.WebData import WebData
from django.utils.html import format_html


def count_ticket_footer(table):
    try:
        c = 0
        for i in table.data:
            c = c + 1
    except Exception as e:
        print(str(e))
        raise
    return f'Total: {c}'


class IncidentsOpenTable(tables.Table):
    number = tables.Column(verbose_name="Ticket")
    u_issue_start_date = tables.Column(verbose_name="Hora Inicio")
    priority = tables.Column(verbose_name="Prioridad")
    category = tables.Column(verbose_name="Categoría")
    short_description = tables.Column(verbose_name="Descripción")
    state = tables.Column(verbose_name="Estado del Ticket")
    Impacted_Services = tables.Column(verbose_name="Servicios")
    Service_Offerings = tables.Column(verbose_name="Servicios Afectados")
    Affected_CIs = tables.Column(verbose_name="CI Afectados")
    assignment_group = tables.Column(verbose_name="Grupo de Soporte")
    time_acum = tables.Column(verbose_name="Tiempo Acumulado")

    def render_short_description(self, value, record):
        return format_html(f"<p>{value}<br><span class='d-inline-block text-truncate' style='max-width: 500px;'>{record['description']}</span></p>")
    
    class Meta:
        fields = ("number","u_issue_start_date", "category", "short_description", "state", "priority", "Impacted_Services", "Service_Offerings", "Affected_CIs","assignment_group")
        empty_text= format_html(f'<p>{WebData.MSG_DATA}</p>')

class MasivosNewTable(tables.Table):
    number = tables.Column(verbose_name="Ticket")
    u_issue_start_date = tables.Column(verbose_name="Hora Inicio")
    category = tables.Column(verbose_name="Categoría")
    short_description = tables.Column(verbose_name="Descripción")
    state = tables.Column(verbose_name="Estado del Ticket")
    priority = tables.Column(verbose_name="Prioridad")
    Impacted_Services = tables.Column(verbose_name="Servicios")
    u_country = tables.Column(verbose_name="País")
    time_acum = tables.Column(verbose_name="Tiempo Acumulado")

    class Meta:
        fields = ("number", "u_issue_start_date", "category", "short_description", "state", "priority", "Impacted_Services", "u_country")
        empty_text= format_html(f'<p>{WebData.MSG_DATA}</p>')

class IncidentsClosedTable(tables.Table):
    number = tables.Column(verbose_name="Ticket",attrs=WebData.COLOR_TABLE_HEADER)
    u_issue_start_date = tables.Column(verbose_name="Hora Inicio",attrs=WebData.COLOR_TABLE_HEADER)
    u_issue_end_date = tables.Column(verbose_name="Hora Fin",attrs=WebData.COLOR_TABLE_HEADER)
    category = tables.Column(verbose_name="Categoría",attrs=WebData.COLOR_TABLE_HEADER)
    short_description = tables.Column(verbose_name="Título",attrs=WebData.COLOR_TABLE_HEADER)
    state = tables.Column(verbose_name="Estado del Ticket",attrs=WebData.COLOR_TABLE_HEADER)
    priority = tables.Column(verbose_name="Prioridad",attrs=WebData.COLOR_TABLE_HEADER)
    Impacted_Services = tables.Column(verbose_name="Servicios",attrs=WebData.COLOR_TABLE_HEADER)
    Service_Offerings = tables.Column(verbose_name="Servicios Afectados",attrs=WebData.COLOR_TABLE_HEADER)
    Affected_CIs = tables.Column(verbose_name="CI Afectados",attrs=WebData.COLOR_TABLE_HEADER)

    class Meta:
        empty_text= format_html(f'<p>{WebData.MSG_DATA}</p>')

