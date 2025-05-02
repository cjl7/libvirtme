from ninja import NinjaAPI, ModelSchema
from inventory.models import VirtualHost
api = NinjaAPI()

class DomSchema(ModelSchema):
    class Meta:
        model = VirtualHost
        fields = ['id', 'name', 'vcpus', 'memory', 'disk', 'disk_used', 'state']


class PhysicalHostSchema(ModelSchema):
    class Meta:
        model = VirtualHost
        fields = ['id', 'name', 'vcpus', 'memory', 'disk', 'disk_used', 'state']

@api.get("/dom", response=DomSchema)
def dom(request, type: str, id: int = 0, name: str = None ):
    if type == 'id':
        doms = VirtualHost.objects.get(id=id)
        return doms
    elif type == 'name':
        doms = VirtualHost.objects.get(name=name)
        return doms
    else:
        return

@api.get("/dom/all", response=list[DomSchema])
def dom(request):
    doms = VirtualHost.objects.all()
    return doms


@api.get("/dom/all", response=list[DomSchema])
def dom(request):
    doms = VirtualHost.objects.all()
    return doms
