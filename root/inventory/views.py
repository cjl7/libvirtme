import re

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import PhysicalHost

# Create your views here.
from django.http import HttpResponse
import libvirt

def make_connection(host):
    conn = libvirt.open(host.connection_string)
    if not conn:
        raise SystemExit("failed to connect to libvirt")
    return conn

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
        all_hosts.append([host, conn.listAllDomains().__len__(), conn.getInfo()])

    return render(request, "inventory/hosts.html", {
        "all_hosts": all_hosts
    })

def view_host(request, id):
    """Show information about a single host"""
    host = PhysicalHost.objects.get(id=id)

    conn = make_connection(host)

    info = conn.getInfo()
    devs = conn.listAllDevices()
    doms = conn.listAllDomains()

    return render(request, "inventory/view_host.html", {
        "host": host,
        "info": info,
        "doms": doms,
        "devs": devs,
        })

def view_domain(request, domid, physicalhostid):
    """Show information about a single domain"""
    conn = make_connection(PhysicalHost.objects.get(id=int(physicalhostid)))
    domain = conn.lookupByID(int(domid))

    # blockinfo = domain.blockInfo(path=)

    return render(request, "inventory/view_domain.html", {
        "domain": domain,
        "blockinfo": blockinfo
        })
