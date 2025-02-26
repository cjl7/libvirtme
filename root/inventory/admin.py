from django.contrib import admin
from .models import PhysicalHost

@admin.register(PhysicalHost)
class PhysicalHostAdmin(admin.ModelAdmin):
    pass

