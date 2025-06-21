from import_export import resources
from .models import Cmts, Node, Source, Electric, City

class NodeResource(resources.ModelResource):

  #def get_export_headers(self):
  #  headers = super().get_export_headers()
  #  for i, h in enumerate(headers):
  #    if h == 'cmts':
  #      headers[i] = "id_cmts"
  #  return headers

  class Meta:
    model = Node

class CmtsResource(resources.ModelResource):

  class Meta:
    model = Cmts

class SourceResource(resources.ModelResource):

  class Meta:
    model = Source

class ElectricResource(resources.ModelResource):
  class Meta:
    model = Electric

class CityResource(resources.ModelResource):
  class Meta:
    model = City
