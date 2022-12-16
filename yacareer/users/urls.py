from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.urls import path, re_path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
    path('password_change/',
         PasswordChangeView.
         as_view(template_name='users/password_change.html',
                 success_url=reverse_lazy('users:password_change_done')),
         name='password_change'),
    path('password_change_done/',
         PasswordChangeDoneView
         .as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         PasswordResetDoneView.
         as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/',
         PasswordResetConfirmView.
         as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         PasswordResetCompleteView.
         as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('signup/', views.signup, name="signup"),
    path('', views.user_list, name="user_list"),
    re_path(r'(?P<pk>[1-9]\d*)/$', views.user_detail, name="user_detail"),
    path('profile/', views.profile, name="profile"),
]
