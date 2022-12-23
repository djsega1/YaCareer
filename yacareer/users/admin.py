from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup

from users.forms import CreateProfileForm, UpdateProfileForm
from users.models import User, UserLinks, UserMedia


class ProfileLinksInline(admin.TabularInline):
    model = UserLinks


class ProfileManagerInline(admin.TabularInline):
    model = UserMedia


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    model = User
    form = UpdateProfileForm
    add_form = CreateProfileForm
    list_display = ('email', 'first_name', 'is_superuser', 'image_tmb_small')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    inlines = (
        ProfileLinksInline,
        ProfileManagerInline,
    )
    fieldsets = (
        (
            'Данные профиля',
            {
                'fields': (
                    'email',
                    'password',
                    'about',
                    'photo',
                    'is_open_to_work',
                ),
            },
        ),
        (
            'Персональные данные',
            {
                'fields': (
                    'birthday',
                    'first_name',
                    'last_name',
                ),
            },
        ),
        (
            'Права доступа',
            {
                'fields': (
                    'is_superuser',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )
    search_fields = ('email',)

    def image_tmb_small(self, obj):
        if obj:
            return obj.image_tmb_small()
        return 'Нет изображения'


admin.site.unregister(DjangoGroup)
