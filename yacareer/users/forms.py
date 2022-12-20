from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core.forms import BaseModelForm
from users.models import User, UserMedia, UserLinks

BOOLEAN_CHOICES = [(True, 'Да'), (False, 'Нет')]


class CreateProfileForm(UserCreationForm, BaseModelForm):

    class Meta:
        model = User
        fields = ('email',)


class UpdateProfileForm(UserChangeForm, BaseModelForm):
    password = None

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'birthday',
            'photo',
            'about',
            'is_open_to_work',
        )
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'is_open_to_work': forms.Select(choices=BOOLEAN_CHOICES),
        }


class ProfileMediaForm(BaseModelForm):

    class Meta:
        model = UserMedia
        fields = ('name', 'description', 'file',)


class ProfileLinksForm(BaseModelForm):

    class Meta:
        model = UserLinks
        fields = ('service', 'slug',)
