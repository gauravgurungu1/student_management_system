from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.attendance_dashboard,
        name='attendance_dashboard'
    ),

    path(
        'save/',
        views.save_attendance,
        name='save_attendance'
    ),

    path(
        'history/',
        views.attendance_history,
        name='attendance_history'
    ),
]