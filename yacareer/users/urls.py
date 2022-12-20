from django.urls import path, re_path

from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    re_path(
        r'(?P<pk>[1-9]\d*)/$',
        views.UserDetailView.as_view(),
        name='user_detail',
    ),
    re_path(
        r'^profile/del_link/(?P<pk>[1-9]\d*)/$',
        views.DeleteLinkView.as_view(),
        name='del_link',
    ),
    re_path(
        r'^profile/del_media/(?P<pk>[1-9]\d*)/$',
        views.DeleteMediaView.as_view(),
        name='del_media',
    ),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
