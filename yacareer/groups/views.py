import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from groups.forms import GroupForm
from groups.models import Group, GroupMembers
from posts.forms import GroupVacancyForm
from posts.models import GroupVacancy


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
                    name__contains=searched
                    )
            )
        return queryset


class GroupDetailView(DetailView):
    template_name = 'groups/group_detail.html'
    model = Group
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        group = get_object_or_404(
            self.model.objects,
            pk=self.kwargs['pk'],
        )
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
        else:
            GroupMembers.objects.create(
                group=group,
                user=request.user,
            )
        return redirect('groups:group_detail', pk)


class CreateGroupView(CreateView, FormView):
    template_name = 'groups/create.html'
    model = Group
    form_class = GroupForm

    def form_valid(self, form):
        new_group = Group.objects.create(
            owner_id=self.request.user.id,
            **form.cleaned_data,
        )
        return redirect('groups:group_detail', new_group.id)


class EditGroupView(UpdateView):
    template_name = 'groups/edit.html'
    model = Group
    form_class = GroupForm
    object = None

    def get_context_data(self, **kwargs):
        group = get_object_or_404(
            self.model.objects,
            pk=self.kwargs['pk'],
        )
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
        formpoints = {
            'group_vacancy_form': self.vacancy_form,
            'group_profile_form': self.profile_form,
        }
        for endpoint, form in formpoints.items():
            if endpoint in request.POST:
                form(request, pk)
                break
        return redirect('groups:group_detail', pk)

    def vacancy_form(self, request, pk):
        group = get_object_or_404(
            self.model.objects,
            pk=pk,
        )
        if group.owner == request.user:
            form = GroupVacancyForm(
                *(request.POST, request.FILES) or None,
            )
            if form.is_valid():
                form.cleaned_data['group_id'] = group.id
                if type(form.cleaned_data['photo']) is InMemoryUploadedFile:
                    old_image = group.photo
                    if old_image:
                        image_path = old_image.path
                        if os.path.exists(image_path):
                            os.remove(image_path)
                GroupVacancy.objects.create(
                    **form.cleaned_data
                )

    def profile_form(self, request, pk):
        group = get_object_or_404(
            self.model.objects,
            pk=pk,
        )
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


class DeleteGroupView(DeleteView):
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
            return super().post(request, pk)
        return redirect('groups:group_detail', pk)


class GroupVacancyView(ListView):
    template_name = 'groups/vacancy/index.html'
    model = GroupVacancy
    context_object_name = 'vacancy_list'
    paginate_by = 9
