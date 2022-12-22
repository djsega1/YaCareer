from django.views.generic import ListView
from posts.models import GroupVacancy


class GroupVacancyView(ListView):
    template_name = 'groups/vacancy/vacancies.html'
    model = GroupVacancy
    context_object_name = 'vacancy_list'
    paginate_by = 9
