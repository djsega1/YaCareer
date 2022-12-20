from django.contrib import admin

from users.forms import UpdateProfileForm, CreateProfileForm
from users.models import Profile, ProfileLinks, ProfileMedia


class ProfileLinksInline(admin.TabularInline):
    model = ProfileLinks


class ProfileManagerInline(admin.TabularInline):
    model = ProfileMedia


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    form = UpdateProfileForm
    add_form = CreateProfileForm
    list_display = ('email', 'first_name', 'is_superuser', 'image_tmb_small')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    inlines = [
        ProfileLinksInline,
        ProfileManagerInline,
    ]
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
    ordering = ('email',)

    def image_tmb_small(self, obj):
        if obj:
            return obj.image_tmb_small()
        return 'Нет изображения'
