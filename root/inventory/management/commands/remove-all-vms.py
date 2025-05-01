from django.core.management.base import BaseCommand, CommandError
from inventory.models import VirtualHost, PhysicalHost
from inventory.views import make_connection


class Command(BaseCommand):
    help = "Remove all virtual hosts"

    def handle(self, *args, **options):
        VirtualHost.objects.all().delete()
