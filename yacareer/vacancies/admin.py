from django.contrib import admin

from vacancies.models import GroupVacancy


@admin.register(GroupVacancy)
class GroupVacancyAdmin(admin.ModelAdmin):
    model = GroupVacancy
    list_display = ('vacancy_name', 'group')
    list_filter = ('group',)
