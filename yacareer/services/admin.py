from django.contrib import admin

from users.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image_tmb_small',
    )

    def image_tmb_small(self, obj):
        if obj:
            return obj.image_tmb_small()
        return 'Нет изображения'
