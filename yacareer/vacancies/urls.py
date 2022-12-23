from django.urls import path, re_path

from vacancies import views

app_name = 'vacancies'

urlpatterns = (
    path('', views.VacancyListView.as_view(), name='vacancy_list'),
    re_path(
        r'^(?P<pk>[1-9]\d*)/$',
        views.VacancyDetailView.as_view(),
        name='vacancy_detail',
    ),
    re_path(
        r'^groups/(?P<pk>[1-9]\d*)/$',
        views.GroupVacancyView.as_view(),
        name='vacancies_of_group',
    ),
)
