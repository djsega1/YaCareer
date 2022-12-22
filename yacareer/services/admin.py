from django.contrib import admin

from users.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'bootstrap_icon',
        'is_contact',
    )
