from django.views.generic import DetailView

from groups.models import Group


class GroupDetailView(DetailView):
    template_name = 'groups/group_detail.html'
    model = Group
    context_object_name = 'group'
