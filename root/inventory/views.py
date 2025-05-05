from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import PhysicalHost, VirtualHost
from django.db.models import Sum
import libvirt

def make_connection(host):
    conn = libvirt.openReadOnly(host.connection_string)
    if not conn:
        raise SystemExit("failed to connect to libvirt")
    return conn

def doms(request):
    all_doms = VirtualHost.objects.all()

    return render(request, "inventory/dom.html", {
        "all_doms": all_doms
    })


@cache_page(10 * 1)
def index(request):

    all_hosts = PhysicalHost.objects.all()
    all_doms = []
    for host in all_hosts:
        conn = make_connection(host)
        doms = conn.listAllDomains()
        for dom in doms:
            dom.physicalhost = host

            all_doms.append(dom)

    return render(request, "inventory/index.html", {
        "all_hosts": all_hosts,
        "all_doms": all_doms
        })

def all_hosts(request):
    all_hosts = []

    for host in PhysicalHost.objects.all():
        conn = make_connection(host)
        all_hosts.append([host, conn.getInfo()])

    return render(request, "inventory/hosts.html", {
        "all_hosts": all_hosts
    })

def view_host(request, id):
    """Show information about a single host"""
    host = PhysicalHost.objects.get(id=id)

    conn = make_connection(host)

    info = conn.getInfo()
    devs = conn.listAllDevices()
    doms = VirtualHost.objects.filter(physical_host=host)
    total_dom_cpu = VirtualHost.objects.filter(physical_host=host).aggregate(Sum('vcpus'))
    total_dom_memory = VirtualHost.objects.filter(physical_host=host).aggregate(Sum('memory'))
    total_dom_disk = VirtualHost.objects.filter(physical_host=host).aggregate(Sum('disk'))
    total_dom_disk_used = VirtualHost.objects.filter(physical_host=host).aggregate(Sum('disk_used'))

    return render(request, "inventory/view_host.html", {
        "host": host,
        "info": info,
        "doms": doms,
        "devs": devs,
        "total_dom_cpu": total_dom_cpu,
        "total_dom_memory": total_dom_memory,
        "total_dom_disk": total_dom_disk,
        "total_dom_disk_used": total_dom_disk_used
        })

def view_domain(request, domid):
    """Show information about a single domain"""
    domain = VirtualHost.objects.get(id=domid)

    return render(request, "inventory/view_domain.html", {
        "domain": domain,
        })
