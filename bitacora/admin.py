from django.contrib import admin
from .models import City, Cmts, Node, Electric, Source
from import_export.admin import ImportExportModelAdmin
from .resources import CityResource, CmtsResource, NodeResource, ElectricResource, SourceResource


class CmtsAdmin(ImportExportModelAdmin):
  resource_class = CmtsResource

class CityAdmin(ImportExportModelAdmin):
  resource_class = CityResource

class ElectricAdmin(ImportExportModelAdmin):
  resource_class = ElectricResource

class SourceAdmin(ImportExportModelAdmin):
  resource_class = SourceResource

class NodeAdmin(ImportExportModelAdmin):
  resource_class = NodeResource


admin.site.register(Cmts, CmtsAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Electric, ElectricAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Node, NodeAdmin)
