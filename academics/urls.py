from django.urls import path
from . import views


urlpatterns = [
    path('', views.academics_dashboard, name='academics_dashboard'),

    path(
        'academic-year/add/',
        views.academic_year_create,
        name='academic_year_create'
    ),

    path(
        'class/add/',
        views.class_create,
        name='class_create'
    ),

    path(
        'section/add/',
        views.section_create,
        name='section_create'
    ),

    path(
        'subject/add/',
        views.subject_create,
        name='subject_create'
    ),

    path(
        'subject/<int:pk>/delete/',
        views.subject_delete,
        name='subject_delete'
    ),
]