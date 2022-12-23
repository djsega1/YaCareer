from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView

from vacancies.forms import RespondForm
from vacancies.models import GroupVacancy


class VacancyDetailView(FormView):
    template_name = 'vacancies/vacancy_detail.html'
    model = GroupVacancy
    form_class = RespondForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = get_object_or_404(
            self.model.objects,
            pk=self.kwargs['pk'],
        )
        context['vacancy'] = vacancy
        return context

    def post(self, request, pk):
        forms_points = {
            'del_vacancy': self.del_vacancy_form,
            'respond': self.respond_form,
        }
        for endpoint, form in forms_points.items():
            if endpoint in request.POST:
                return form(request, pk)
        return redirect('groups:group_detail', pk)

    def del_vacancy_form(self, request, pk):
        group = get_object_or_404(
            self.model.objects,
            pk=pk,
        ).group
        if group.owner == request.user:
            self.model.objects.filter(pk=pk).delete()
        return redirect('vacancies:vacancies_of_group', group.id)

    def respond_form(self, request, pk):
        form = RespondForm(request.POST)
        if form.is_valid():
            owner = get_object_or_404(
                self.model.objects,
                pk=pk,
            ).group.owner
            send_mail(
                f'Отклик на вакансию {pk}',
                form.cleaned_data['text'],
                self.request.user.email,
                (owner.email,),
                fail_silently=True,
            )
        return redirect('groups:group_detail', pk)


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
