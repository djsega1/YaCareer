import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from users.forms import (DeleteProfileLinksForm, DeleteProfileMediaForm,
                         ProfileLinksForm, ProfileMediaForm, UpdateProfileForm)
from users.models import User, UserLinks, UserMedia


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    form_class = UpdateProfileForm
    model = User
    success_url = reverse_lazy('homepage:home')

    def get_context_data(self, **kwargs):
        profile_form = self.form_class(
            initial=self.initial,
            instance=self.request.user,
        )
        del_media_form = DeleteProfileMediaForm(self.request.user)
        del_links_form = DeleteProfileLinksForm(self.request.user)
        return {
            'profile_form': profile_form,
            'media_form': ProfileMediaForm(),
            'del_media_form': del_media_form,
            'links_form': ProfileLinksForm(),
            'del_links_form': del_links_form,
        }

    def post(self, request):
        formpoints = {
            'profile_submit': self.profile_form,
            'media_submit': self.media_form,
            'links_submit': self.links_form,
            'media_del': self.del_media_form,
            'links_del': self.del_links_form,
        }
        for endpoint, form in formpoints.items():
            if endpoint in request.POST:
                form(request)
                break
        return redirect('homepage:home')

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
                old_image = request.user.photo
                if old_image:
                    image_path = old_image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
            form.save()

    def del_media_form(self, request):
        form = DeleteProfileMediaForm(
            request.user,
            request.POST or None,
        )
        if form.is_valid():
            UserMedia.objects.filter(
                user=request.user,
                **form.cleaned_data,
            ).delete()

    def del_links_form(self, request):
        form = DeleteProfileLinksForm(
            request.user,
            request.POST or None,
        )
        if form.is_valid():
            UserLinks.objects.filter(
                user=request.user,
                **form.cleaned_data,
            ).delete()
