from import_export import resources
from .models import Work

class WorkResource(resources.ModelResource):
    class meta:
        model = Work
