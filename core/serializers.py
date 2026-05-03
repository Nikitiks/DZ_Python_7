from django.core.serializers.json import DjangoJSONEncoder
from .models import Task

class TaskSerializer(DjangoJSONEncoder):
    def default(self, o:Task):
        result = {}
        result["id"] = o.id
        result["header"] = o.header
        result["text"] = o.header
        result["date_start"] = o.date_start
        result["date_end"] = o.date_end
        return result
