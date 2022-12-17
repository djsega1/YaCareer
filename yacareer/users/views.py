from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import CreateProfileForm, UpdateProfileForm
from users.models import Profile


class SignUpView(FormView):
    template_name = 'users/signup.html'
    model = Profile
    form_class = CreateProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    form_class = UpdateProfileForm
    model = Profile
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        form = self.form_class(
            initial=self.initial,
            instance=self.request.user,
        )
        return {'form': form}

    def post(self, request):
        form = self.form_class(
            request.POST or None,
            instance=request.user,
        )
        if form.is_valid():
            self.model.objects.filter(id=request.user.id).update(
                **form.cleaned_data,
            )
        return redirect('users:profile')
