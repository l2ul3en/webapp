from import_export import resources
from .models import Node

class NodeResource(resources.ModelResource):
    class Meta:
        model = Node
