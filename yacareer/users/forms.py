from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core.forms import BaseModelForm
from users.models import FollowsU2U, User, UserLinks, UserMedia

BOOLEAN_CHOICES = ((True, 'Да'), (False, 'Нет'))


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


class DeleteProfileMediaForm(forms.Form):
    file = forms.ChoiceField(label='Файл')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        media_of_user = [
            (i.file, i.name) for i in user.media.all()
        ]
        self.fields['file'].choices = media_of_user
        self.fields['file'].widget.attrs['class'] = 'form-control'


class ProfileLinksForm(BaseModelForm):

    class Meta:
        model = UserLinks
        fields = ('service', 'slug')


class DeleteProfileLinksForm(forms.Form):
    slug = forms.ChoiceField(label='Ссылка')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        links_of_user = [
            (i.slug, i.slug) for i in user.links.all()
        ]
        self.fields['slug'].choices = links_of_user
        self.fields['slug'].widget.attrs['class'] = 'form-control'


class FollowsU2UForm(BaseModelForm):

    class Meta:
        model = FollowsU2U
        fields = ('to_user', 'from_user')
