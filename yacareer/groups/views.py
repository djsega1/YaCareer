# import os

# from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, UpdateView

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


class EditGroupView(DetailView, UpdateView):
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

    def get_context_data(self, **kwargs):
        form = GroupForm(
            initial=self.initial,
            instance=kwargs['object'],
        )
        return {'form': form}
