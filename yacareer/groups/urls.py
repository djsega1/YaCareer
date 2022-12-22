from django.urls import path, re_path

from groups import views
from posts.views import GroupVacancyView

app_name = 'groups'

urlpatterns = [
    path(
        '',
        views.GroupListView.as_view(),
        name='group_list',
    ),
    path(
        'create/',
        views.CreateGroupView.as_view(),
        name='create',
    ),
    re_path(
        r'^(?P<pk>[1-9]\d*)/delete/$',
        views.DeleteGroupView.as_view(),
        name='delete',
    ),
    re_path(
        r'^(?P<pk>[1-9]\d*)/edit/$',
        views.EditGroupView.as_view(),
        name='edit',
    ),
    re_path(
        r'(?P<pk>[1-9]\d*)/$',
        views.GroupDetailView.as_view(),
        name='group_detail',
    ),
    re_path(
        r'(?P<pk>[1-9]\d*)/vacancy/$',
        GroupVacancyView.as_view(),
        name='vacancy_list',
    ),
]
