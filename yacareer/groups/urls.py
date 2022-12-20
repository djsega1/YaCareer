from django.urls import path, re_path

from groups import views

app_name = 'groups'

urlpatterns = [
    # path(
    #     'group_list',
    #     views.GroupListView.as_view(),
    #     name='group_list',
    # ),
    path(
        'create/',
        views.CreateGroupView.as_view(),
        name='create',
    ),
    # re_path(
    #     '^delete/(?P<pk>[1-9]\d*)/$',
    #     views.DeleteGroupView.as_view(),
    #     name='delete',
    # ),
    re_path(
        r'(?P<pk>[1-9]\d*)/$',
        views.GroupDetailView.as_view(),
        name='group_detail',
    ),
]
