from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import (
    CreateProfileForm,
    UpdateProfileForm,
    ProfileMediaForm,
    ProfileLinksCreateForm,
)
from users.models import Profile, ProfileLinks


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
        profile_form = self.form_class(
            initial=self.initial,
            instance=self.request.user,
        )
        media_form = ProfileMediaForm(
            initial=self.initial,
            instance=self.request.user,
        )
        links_form = ProfileLinksCreateForm(
            initial=self.initial,
            instance=self.request.user,
        )
        return {
            'profileform': profile_form,
            'mediaform': media_form,
            'linksform': links_form,
        }

    def post(self, request):
        self.profile_form(request)
        self.link_form(request)
        self.media_form(request)
        # self.del_link_form(request)
        return redirect('users:profile')

    def link_form(self, request):
        form = ProfileLinksCreateForm(
            request.POST or None,
            instance=request.user,
        )
        if form.is_valid():
            ProfileLinks.objects.create(
                profile_id=request.user.id,
                **form.cleaned_data,
            )

    # def del_link_form(self, request):
    #     form = ProfileLinksDeleteForm(
    #         request.POST or None,
    #         instance=request.user,
    #     )
    #     print(form.cleaned_data)

    def media_form(self, request):
        ...
        # form = self.form_class(
        #     request.POST, request.FILES or None,
        #     instance=request.user,
        # )
        # if form.is_valid():
        #     file = form.cleaned_data['photo']
        #     if file:
        #         fs = FileSystemStorage()
        #         fs.save(file.name, file)
        #     form.save()

    def profile_form(self, request):
        form = self.form_class(
            request.POST, request.FILES or None,
            instance=request.user,
        )
        if form.is_valid():
            file = form.cleaned_data['photo']
            if file:
                fs = FileSystemStorage()
                fs.save(file.name, file)
            self.model.objects.filter(id=request.user.id).update(
                **form.cleaned_data,
            )
