import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  UpdateView)

from groups.forms import GroupForm
from groups.models import Group


class GroupDetailView(DetailView):
    template_name = 'groups/group_detail.html'
    model = Group
    context_object_name = 'group'


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

    def get_success_url(self):
        return reverse_lazy(
            'groups:group_detail',
            args=(
                self.kwargs['pk'],
            )
        )

    def form_valid(self, form):
        print(form.cleaned_data)
        if type(form.cleaned_data['photo']) is InMemoryUploadedFile:
            old_image = get_object_or_404(
                self.model.objects,
                pk=self.kwargs['pk'],
            ).photo
            if old_image:
                image_path = old_image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
        form.save()
        return redirect('groups:group_detail', self.kwargs['pk'])


class DeleteGroupView(DeleteView):
    template_name = 'groups/delete.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('users:profile')
