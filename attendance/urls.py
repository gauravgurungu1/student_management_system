from django.urls import path

from . import views

urlpatterns = [
    path("", views.attendance_list, name="attendance_list"),
    path("mark/", views.attendance_create, name="attendance_create"),
    path("session/<int:id>/", views.attendance_detail, name="attendance_detail"),
    path("student/<int:id>/", views.student_attendance_history, name="student_attendance_history"),
]
