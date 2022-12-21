from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm

from core.forms import BaseModelForm
from users.models import FollowsU2U, User, UserLinks, UserMedia

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
        fields = ('name', 'description', 'file')


class DeleteProfileMediaForm(BaseModelForm):

    class Meta:
        model = UserMedia
        fields = ('file',)


class ProfileLinksForm(BaseModelForm):

    class Meta:
        model = UserLinks
        fields = ('service', 'slug')


class DeleteProfileLinksForm(BaseModelForm):

    class Meta:
        model = UserLinks
        fields = ('id', 'slug')


class FollowsU2UForm(ModelForm):

    class Meta:
        model = FollowsU2U
        fields = ('to_user', 'from_user')
