from core.forms import BaseModelForm
from posts.models import GroupVacancy, UserPost


class UserPostForm(BaseModelForm):

    class Meta:
        model = UserPost
        fields = ('photo', 'text',)


class GroupVacancyForm(BaseModelForm):

    class Meta:
        model = GroupVacancy
        fields = ('text',)
