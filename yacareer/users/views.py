from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import FormMixin

from users.forms import CreateProfileForm, FollowsU2UForm
from users.models import FollowsU2U, User


class SignUpView(FormView):
    template_name = 'users/signup.html'
    model = User
    form_class = CreateProfileForm
    success_url = reverse_lazy('homepage:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserListView(ListView):
    template_name = 'users/user_list.html'
    model = User
    context_object_name = 'user_list'
    paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset()
        searched = self.request.GET.get('searched', '')
        if searched:
            searched = searched.lower()
            queryset = (
                queryset.
                filter(
                    Q(first_name__icontains=searched)
                    | Q(last_name__icontains=searched)
                    | Q(email__icontains=searched)
                    )
            )
        return queryset


class UserDetailView(DetailView, FormMixin):
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        for i in self.object.user_followed.all():
            if self.request.user == i.from_user:
                data['is_followed'] = True
                break
        else:
            data['is_followed'] = False
        return data

    def post(self, request, pk):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            FollowsU2U.objects.filter(
                **form.cleaned_data
            ).delete()
        return redirect('users:user_detail', pk)
