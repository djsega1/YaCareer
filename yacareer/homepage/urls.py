from django.urls import path

from homepage import views

app_name = 'homepage'

urlpatterns = [
    path(
        '',
        views.ProfileView.as_view(),
        name='home',
    )
]
