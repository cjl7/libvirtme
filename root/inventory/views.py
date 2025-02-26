from django.shortcuts import render

from .models import PhysicalHost

# Create your views here.
import libvirt

def index(request):

    all_hosts = PhysicalHost.objects.all()
    all_doms = []
    for host in all_hosts:
        conn = libvirt.open(host.connection_string)
        if not conn:
            raise SystemExit("failed to connect to libvirt")

        doms = conn.listAllDomains()
        all_doms.append(doms)

    return render(request, "inventory/index.html", {
        "all_hosts": all_hosts,
        "all_doms": all_doms
        })

def view_host(request, id):
    """Show information about a single host"""
    host = PhysicalHost.objects.get(id=id)
    
    conn = libvirt.openReadOnly(host.connection_string)
    if not conn:
        raise SystemExit("failed to connect to libvirt")

    info = conn.getInfo()
    doms = conn.listAllDomains()

    return render(request, "inventory/view_host.html", {
        "host": host,
        "info": info,
        "doms": doms
        })
