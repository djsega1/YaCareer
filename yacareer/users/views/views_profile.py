import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from users.forms import (
    ProfileLinksForm,
    ProfileMediaForm,
    UpdateProfileForm,
)
from users.models import User, UserLinks, UserMedia


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    form_class = UpdateProfileForm
    model = User
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        profile_form = self.form_class(
            initial=self.initial,
            instance=self.request.user,
        )
        media_form = ProfileMediaForm()
        links_form = ProfileLinksForm()
        return {
            'profile_form': profile_form,
            'media_form': media_form,
            'links_form': links_form,
        }

    def post(self, request):
        endpoints = {
            'profile_submit': self.profile_form,
            'media_submit': self.media_form,
            'links_submit': self.links_form,
        }
        for endpoint, form in endpoints.items():
            if endpoint in request.POST:
                form(request)
        return redirect('users:profile')

    def links_form(self, request):
        form = ProfileLinksForm(
            request.POST or None,
            instance=request.user,
        )
        if form.is_valid():
            UserLinks.objects.create(
                user_id=request.user.id,
                **form.cleaned_data,
            )

    def media_form(self, request):
        form = ProfileMediaForm(
            *(request.POST, request.FILES) or None,
            instance=request.user,
        )
        if form.is_valid():
            UserMedia.objects.create(
                user_id=request.user.id,
                **form.cleaned_data,
            )

    def profile_form(self, request):
        form = self.form_class(
            *(request.POST, request.FILES) or None,
            instance=request.user,
        )
        if form.is_valid():
            if type(form.cleaned_data['photo']) is InMemoryUploadedFile:
                old_image = get_object_or_404(
                    self.model.objects,
                    pk=request.user.id,
                ).photo
                if old_image:
                    image_path = old_image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
            form.save()


class DeleteLinkView(LoginRequiredMixin, DetailView):
    model = UserLinks

    def get(self, request, pk):
        self.model.objects.filter(
            pk=pk,
            user_id=request.user.id,
        ).delete()
        return redirect('users:profile')


class DeleteMediaView(LoginRequiredMixin, DetailView):
    model = UserMedia

    def get(self, request, pk):
        file = get_object_or_404(
            self.model.objects,
            pk=pk,
            user_id=request.user.id,
        ).file
        file_path = file.path
        if os.path.exists(file_path):
            os.remove(file_path)
        self.model.objects.filter(
            pk=pk,
            user_id=request.user.id,
        ).delete()
        return redirect('users:profile')
