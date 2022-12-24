from core.forms import BaseModelForm
from groups.models import Group


class GroupForm(BaseModelForm):

    class Meta:
        model = Group
        fields = ('name', 'photo', 'about')
        labels = {
            'name': 'Название',
            'photo': 'Фото группы',
            'about': 'О группе',
        }
