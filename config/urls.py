from django.contrib import admin
from django.urls import include, path

from accounts import views


urlpatterns = [

    # Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Authentication
    path(
        'accounts/',
        include('accounts.urls')
    ),

    # Dashboard
    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    # Students
    path(
        'students/',
        include('students.urls')
    ),

    # Academics
    path(
        'academics/',
        include('academics.urls')
    ),

    # Teachers
    path(
        'teachers/',
        include('teachers.urls')
    ),

    # Attendance
    path(
        'attendance/',
        include('attendance.urls')
    ),

    # Fees
    path(
        'fees/',
        include('fees.urls')
    ),

    # Payments
    path(
        'payments/',
        include('payments.urls')
    ),
]