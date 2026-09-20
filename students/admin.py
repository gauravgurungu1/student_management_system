from django.contrib import admin

from .models import Student, Guardian


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'get_student_name',
        'gender',
        'class_name',
        'section',
        'academic_year',
        'phone',
        'is_active',
    )

    list_filter = (
        'gender',
        'class_name',
        'section',
        'academic_year',
        'is_active',
    )

    search_fields = (
        'student_id',
        'user__first_name',
        'user__last_name',
        'user__email',
        'phone',
    )

    ordering = ('student_id',)

    def get_student_name(self, obj):
        return obj.user.get_full_name()

    get_student_name.short_description = 'Student Name'


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = (
        'get_guardian_name',
        'relation',
        'occupation',
        'address',
    )

    list_filter = (
        'relation',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'occupation',
    )

    def get_guardian_name(self, obj):
        return obj.user.get_full_name()

    get_guardian_name.short_description = 'Guardian Name'