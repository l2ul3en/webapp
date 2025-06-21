from django.contrib import admin
from .models import Node
from import_export.admin import ImportExportModelAdmin
from .resources import NodeResource

class NodeAdmin(ImportExportModelAdmin):
    resource_class = NodeResource

admin.site.register(Node, NodeAdmin)
