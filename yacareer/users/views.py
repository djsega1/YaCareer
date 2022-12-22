import os

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.edit import FormMixin

from posts.forms import UserPostForm
from posts.models import UserPost
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


class UserListView(ListView):
    template_name = 'users/index.html'
    model = User
    context_object_name = 'user_list'
    paginate_by = 24


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
            'user_post_form': UserPostForm(),
        }

    def post(self, request):
        formpoints = {
            'profile_submit': self.profile_form,
            'media_submit': self.media_form,
            'links_submit': self.links_form,
            'media_del': self.del_media_form,
            'links_del': self.del_links_form,
            'post_create': self.post_create,
        }
        for endpoint, form in formpoints.items():
            if endpoint in request.POST:
                form(request)
                break
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
                old_image = request.user.photo
                if old_image:
                    image_path = old_image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
            form.save()

    def post_create(self, request):
        form = UserPostForm(
            *(request.POST, request.FILES) or None,
            instance=request.user,
        )
        if form.is_valid():
            form.cleaned_data['user_id'] = request.user.id
            UserPost.objects.create(
                **form.cleaned_data,
            )

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
