from django.contrib import admin

from vacancies.models import GroupVacancy


@admin.register(GroupVacancy)
class GroupVacancyAdmin(admin.ModelAdmin):
    model = GroupVacancy
    list_display = ('v_name', 'group')
    list_filter = ('group',)
