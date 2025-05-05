from ninja import NinjaAPI, ModelSchema
from inventory.models import VirtualHost, PhysicalHost 
api = NinjaAPI()

class DomSchema(ModelSchema):
    class Meta:
        model = VirtualHost
        fields = ['id', 'name', 'vcpus', 'memory', 'disk', 'disk_used', 'state']


class PhysicalHostSchema(ModelSchema):
    class Meta:
        model = PhysicalHost
        fields = ['id', 'name', 'connection_string']

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
def all_doms(request):
    doms = VirtualHost.objects.all()
    return doms


@api.get("/host/all", response=list[DomSchema])
def all_host(request):
    all_hosts = VirtualHost.objects.all()
    return all_hosts
