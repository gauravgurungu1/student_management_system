from django.contrib import admin

from .models import AttendanceRecord, AttendanceSession


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ("subject", "date", "created_at")
    list_filter = ("date", "subject__course")
    search_fields = ("subject__name", "subject__code", "subject__course__name")
    inlines = [AttendanceRecordInline]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "session", "status")
    list_filter = ("status", "session__date")
    search_fields = ("student__name", "student__email", "session__subject__name")
