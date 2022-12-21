from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import CreateProfileForm
from users.models import User


class SignUpView(FormView):
    template_name = 'users/signup.html'
    model = User
    form_class = CreateProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
