from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from vacancies.forms import RespondForm
from vacancies.models import GroupVacancy


class VacancyDetailView(DetailView, FormMixin):
    template_name = 'vacancies/vacancy_detail.html'
    model = GroupVacancy
    form_class = RespondForm
    context_object_name = 'vacancy'

    def post(self, request, pk):
        forms_points = {
            'del_vacancy': self.del_vacancy_form,
            'respond': self.respond_form,
        }
        vacancy = get_object_or_404(GroupVacancy, pk=pk)
        for endpoint, form in forms_points.items():
            if endpoint in request.POST:
                return form(request, vacancy)
        return redirect('groups:group_detail', pk)

    def del_vacancy_form(self, request, vacancy):
        group = vacancy.group
        if group.owner == request.user:
            vacancy.delete()
        return redirect('vacancies:vacancies_of_group', group.pk)

    def respond_form(self, request, vacancy):
        form = RespondForm(request.POST)
        if form.is_valid():
            send_mail(
                f'Отклик на вакансию {vacancy.vacancy_name}',
                form.cleaned_data['text'],
                self.request.user.email,
                (vacancy.group.owner.email,),
                fail_silently=True,
            )
        return redirect('groups:group_detail', vacancy.group.pk)


class GroupVacancyView(ListView):
    template_name = 'vacancies/vacancy_list.html'
    model = GroupVacancy
    context_object_name = 'vacancy_list'
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().filter(
            group=self.kwargs['pk'],
        )


class VacancyListView(ListView):
    template_name = 'vacancies/vacancy_list.html'
    model = GroupVacancy
    context_object_name = 'vacancy_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        searched = self.request.GET.get('searched', '')
        if searched:
            queryset = (
                queryset.
                filter(
                    Q(vacancy_name__contains=searched)
                    | Q(text__contains=searched)
                    )
            )
        return queryset
