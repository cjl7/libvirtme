from django.core.management.base import BaseCommand, CommandError
from inventory.models import VirtualHost, PhysicalHost
from inventory.views import make_connection
from xml.dom import minidom


class Command(BaseCommand):
    help = "Get all virtual hosts from Physical hosts"

    def handle(self, *args, **options):
        all_hosts = PhysicalHost.objects.all()

        for host in all_hosts:
            try:
                conn = make_connection(host)
                for dom in conn.listAllDomains():
                    # get disk size
                    raw_xml = dom.XMLDesc(0)
                    xml = minidom.parseString(raw_xml)
                    diskTypes = xml.getElementsByTagName('disk')
                    for diskType in diskTypes:
                        if diskType.getAttribute('device') == 'disk':
                            diskNodes = diskType.childNodes
                            for diskNode in diskNodes:
                                if diskNode.nodeName == 'source':
                                    for attr in diskNode.attributes.keys():
                                        if diskNode.attributes[attr].name == 'file':
                                            blkinf = dom.blockInfo(diskNode.attributes[attr].value)

                    obj, created = VirtualHost.objects.update_or_create(
                        name=dom.name(),
                        physical_host=host,
                        state=dom.info()[0],
                        memory=dom.info()[1] / 1024 ** 2,
                        disk=round(blkinf[0] / 1024 ** 3),
                        disk_used=round(blkinf[1] / 1024 ** 3),
                        vcpus=dom.info()[3]
                    )
                    self.stdout.write(
                        self.style.SUCCESS('Successfully imported vm "%s", "%s"' % (dom.name(), obj.id))
                    )
            except Exception as e:
                print("got error: %s - %s", e,dom.name())
                pass

