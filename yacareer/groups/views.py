import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from groups.forms import GroupForm
from groups.models import Group, GroupMembers
from vacancies.forms import GroupVacancyForm
from vacancies.models import GroupVacancy


class GroupListView(ListView):
    template_name = 'groups/group_list.html'
    model = Group
    context_object_name = 'group_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        searched = self.request.GET.get('searched', '')
        if searched:
            queryset = (
                queryset.
                filter(
                    Q(name__lower__contains=searched)
                    | Q(about__lower__contains=searched)
                    )
            )
        return queryset


class GroupDetailView(DetailView):
    template_name = 'groups/group_detail.html'
    model = Group
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        group = self.object
        return {
            'group': group,
        }

    def post(self, request, pk):
        group = get_object_or_404(
            self.model.objects,
            pk=pk,
        )
        followu2g = GroupMembers.objects.filter(
            group=group,
            user=request.user,
        )
        if followu2g:
            followu2g.delete()
            messages.success(request, 'Вы отписались от группы')
        else:
            GroupMembers.objects.create(
                group=group,
                user=request.user,
            )
            messages.success(request, 'Вы подписались на группу')
        return redirect('groups:group_detail', pk)


class CreateGroupView(CreateView, LoginRequiredMixin):
    template_name = 'groups/create.html'
    model = Group
    form_class = GroupForm

    def form_valid(self, form):
        new_group = Group.objects.create(
            owner_id=self.request.user.id,
            **form.cleaned_data,
        )
        messages.success(self.request, 'Поздравляем!!! Вы создали группу')
        return redirect('groups:group_detail', new_group.id)


class EditGroupView(UpdateView, LoginRequiredMixin):
    template_name = 'groups/edit.html'
    model = Group
    form_class = GroupForm

    def get_context_data(self, **kwargs):
        group = self.object
        vacancy = GroupVacancyForm()
        form = self.form_class(
            initial=self.initial,
            instance=group,
        )
        return {
            'group': group,
            'vacancy': vacancy,
            'form': form,
        }

    def get_success_url(self):
        return reverse_lazy(
            'groups:group_detail',
            args=(
                self.kwargs['pk'],
            )
        )

    def post(self, request, pk):
        forms_points = {
            'group_vacancy_form': self.vacancy_form,
            'group_profile_form': self.profile_form,
        }
        group = get_object_or_404(
            self.model.objects,
            pk=pk,
        )
        for endpoint, form in forms_points.items():
            if endpoint in request.POST:
                form(request, group)
                break
        return redirect('groups:group_detail', pk)

    def vacancy_form(self, request, group):
        if group.owner == request.user:
            form = GroupVacancyForm(
                *(request.POST, request.FILES) or None,
            )
            if form.is_valid():
                form.cleaned_data['group_id'] = group.id
                GroupVacancy.objects.create(
                    **form.cleaned_data
                )
                messages.success(request, 'Вакансия создана')

    def profile_form(self, request, group):
        if group.owner == request.user:
            form = self.form_class(
                *(request.POST, request.FILES) or None,
                instance=group,
            )
            if form.is_valid():
                if type(form.cleaned_data['photo']) is InMemoryUploadedFile:
                    old_image = group.photo
                    if old_image:
                        image_path = old_image.path
                        if os.path.exists(image_path):
                            os.remove(image_path)
                form.save()
                messages.success(request, 'Изменения успешно сохранены')


class DeleteGroupView(DeleteView, LoginRequiredMixin):
    template_name = 'groups/delete.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('homepage:home')

    def post(self, request, pk):
        group = get_object_or_404(
            self.model.objects,
            pk=pk,
        )
        if group.owner == self.request.user:
            messages.success(request, 'Группа удалена')
            return super().post(request, pk)
        return redirect('groups:group_detail', pk)
