from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from users.forms import FollowsU2UForm
from users.models import User, FollowsU2U


class UserDetailView(FormView, DetailView):
    template_name = 'users/user_detail.html'
    model = User
    form_class = FollowsU2UForm
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy(
            'users:user_detail',
            args=(
                self.kwargs['pk'],
            )
        )

    def form_valid(self, form):
        form.save()
        return redirect('users:user_detail', self.kwargs['pk'])

    def form_invalid(self, form):
        FollowsU2U.objects.filter(
            **form.cleaned_data
        ).delete()
        return redirect('users:user_detail', self.kwargs['pk'])
