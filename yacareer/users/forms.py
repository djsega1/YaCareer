from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm

from users.models import Profile, ProfileMedia, ProfileLinks

BOOLEAN_CHOICES = [(True, 'Да'), (False, 'Нет')]


class CreateProfileForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profile
        fields = ('email',)


class UpdateProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    password = None

    class Meta:
        model = Profile
        fields = (
            'email',
            'first_name',
            'last_name',
            'birthday',
            'photo',
            'description',
            'is_open_to_work',
        )
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'is_open_to_work': forms.Select(choices=BOOLEAN_CHOICES),
        }


class ProfileMediaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProfileMedia
        fields = ('name', 'description', 'file',)


class ProfileLinksForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProfileLinks
        fields = ('service', 'slug',)
