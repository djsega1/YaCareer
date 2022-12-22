from core.forms import BaseModelForm
from posts.models import UserPost, GroupPost


class UserPostForm(BaseModelForm):

    class Meta:
        model = UserPost
        fields = ('photo', 'text',)


class GroupPostForm(BaseModelForm):

    class Meta:
        model = GroupPost
        fields = ('photo', 'text',)
