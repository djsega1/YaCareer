from django.contrib import admin

from groups.models import Group, GroupMedia, GroupMembers


class GroupMembersInline(admin.TabularInline):
    model = GroupMembers


class GroupMediaInline(admin.TabularInline):
    model = GroupMedia


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('name', 'image_tmb_small')
    ordering = ('members',)
    inlines = [
        GroupMembersInline,
        GroupMediaInline,
    ]
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
    ordering = ('members',)

    def image_tmb_small(self, obj):
        if obj:
            return obj.image_tmb_small()
        return 'Нет изображения'
