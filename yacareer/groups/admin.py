from django.contrib import admin

from groups.models import Group, GroupMembers
from vacancies.models import GroupVacancy


class GroupMembersInline(admin.TabularInline):
    model = GroupMembers


class GroupVacancyInline(admin.TabularInline):
    model = GroupVacancy


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('name', 'image_tmb_small')
    inlines = (
        GroupMembersInline,
        GroupVacancyInline,
    )
    fieldsets = (
        (
            'Данные компании',
            {
                'fields': (
                    'name',
                    'about',
                    'photo',
                    'owner',
                ),
            },
        ),
    )
    search_fields = ('name',)

    def image_tmb_small(self, obj):
        if obj:
            return obj.image_tmb_small()
        return 'Нет изображения'
