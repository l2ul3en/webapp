import django_tables2 as tables
from .models import Node

def suma_footer(table):
    try:
        s = sum(x.subscriber for x in table.data)
    except Exception as e:
        print(str(e))
        raise 
    return f'Total: {s}'

class NodeTable(tables.Table):
    class Meta:
        model = Node
        template_name = "django_tables2/bootstrap5.html"
        exclude = ("id",)

class CoverageTable(tables.Table):
    subscriber = tables.Column(footer=suma_footer)
    class Meta:
        export_formats = ['xls', 'xlsx', 'csv']
        model = Node
        exclude = ('id',)
        template_name = 'django_tables2/bootstrap5.html'
