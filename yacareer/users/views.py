import os

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from users.forms import (
    CreateProfileForm,
    ProfileLinksForm,
    ProfileMediaForm,
    UpdateProfileForm,
)
from users.models import User, UserLinks, UserMedia


class SignUpView(FormView):
    template_name = 'users/signup.html'
    model = User
    form_class = CreateProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserDetailView(DetailView):
    template_name = 'users/user_detail.html'
    model = User
    context_object_name = 'user'


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
            'profileform': profile_form,
            'mediaform': media_form,
            'linksform': links_form,
        }

    def post(self, request):
        if request.FILES.get('file', False):
            self.media_form(request)
        elif 'email' in request.POST:
            self.profile_form(request)
        else:
            self.link_form(request)
        return redirect('users:profile')

    def link_form(self, request):
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
            form.save()

    def profile_form(self, request):
        form = self.form_class(
            *(request.POST, request.FILES) or None,
            instance=request.user,
        )
        if form.is_valid():
            if type(form.cleaned_data['photo']) is InMemoryUploadedFile:
                old_image = get_object_or_404(
                    User.objects,
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
