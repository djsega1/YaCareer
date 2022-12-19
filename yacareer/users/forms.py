from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm

from users.models import Profile, ProfileMedia, ProfileLinks


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
        fields = ('email', 'first_name', 'last_name', 'photo', 'description')


class ProfileMediaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProfileMedia
        fields = ('name', 'description', 'file')
        exclude = ('profile',)


class ProfileLinksForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProfileLinks
        fields = ('service', 'slug')
        exclude = ('profile',)
