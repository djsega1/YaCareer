from django.views.generic import CreateView, DetailView, FormView

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
