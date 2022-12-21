import os

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from users.forms import (CreateProfileForm, DeleteProfileLinksForm,
                         DeleteProfileMediaForm, FollowsU2UForm,
                         ProfileLinksForm, ProfileMediaForm, UpdateProfileForm)
from users.models import FollowsU2U, User, UserLinks, UserMedia


class SignUpView(FormView):
    template_name = 'users/signup.html'
    model = User
    form_class = CreateProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


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
        endpoints = {
            'profile_submit': self.profile_form,
            'media_submit': self.media_form,
            'links_submit': self.links_form,
            'media_del': self.del_media_form,
            'links_del': self.del_links_form,
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
