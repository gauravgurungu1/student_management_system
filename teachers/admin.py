from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'full_name',
        'email',
        'phone',
        'qualification',
        'is_active',
    )

    list_filter = (
        'is_active',
        'subjects',
    )

    search_fields = (
        'employee_id',
        'full_name',
        'email',
        'phone',
    )

    filter_horizontal = (
        'subjects',
    )

    ordering = (
        'employee_id',
    )