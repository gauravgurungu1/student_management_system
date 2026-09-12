from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    path('students/', include('students.urls')),


    path('academics/', include('academics.urls')),

     path('reports/', include('reports.urls')),

     path('attendance/', include('attendance.urls')),


    path('', views.dashboard, name='dashboard'),
]