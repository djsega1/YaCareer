from django.urls import path, re_path

from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    re_path(
        r'^(?P<pk>[1-9]\d*)/$',
        views.UserDetailView.as_view(),
        name='user_detail',
    ),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
