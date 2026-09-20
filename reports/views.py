from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from django.shortcuts import render

from academics.models import AcademicYear, Class, Section, Subject
from students.models import Student


@login_required
def report_dashboard(request):
    search_query = request.GET.get("search", "").strip()
    class_id = request.GET.get("class", "").strip()

    students = Student.objects.select_related(
        "user",
        "academic_year",
        "class_name",
        "section",
    ).all()

    if search_query:
        students = students.filter(
            models.Q(student_id__icontains=search_query)
            | models.Q(user__first_name__icontains=search_query)
            | models.Q(user__last_name__icontains=search_query)
            | models.Q(user__email__icontains=search_query)
        )

    if class_id.isdigit():
        students = students.filter(class_name_id=class_id)
    elif class_id:
        class_id = ""

    students = students.order_by("student_id")

    student_count = Student.objects.count()
    active_student_count = Student.objects.filter(is_active=True).count()

    academic_year_count = AcademicYear.objects.count()
    class_count = Class.objects.count()
    section_count = Section.objects.count()
    subject_count = Subject.objects.count()

    attendance_count = 0

    try:
        from attendance.models import Attendance
        attendance_count = Attendance.objects.count()
    except (ImportError, AttributeError):
        attendance_count = 0

    fee_count = 0
    paid_fees = 0
    partial_fees = 0
    unpaid_fees = 0

    try:
        from fees.models import Fee

        fee_count = Fee.objects.count()

        field_names = [field.name for field in Fee._meta.get_fields()]

        if "status" in field_names:
            paid_fees = Fee.objects.filter(status="paid").count()
            partial_fees = Fee.objects.filter(status="partial").count()
            unpaid_fees = Fee.objects.filter(status="unpaid").count()

    except (ImportError, AttributeError):
        pass

    context = {
        "students": students,
        "classes": Class.objects.all(),

        "class_summary": Class.objects.annotate(
            student_count=Count("students")
        ).order_by("name"),

        "student_count": student_count,
        "active_student_count": active_student_count,
        "academic_year_count": academic_year_count,
        "class_count": class_count,
        "section_count": section_count,
        "subject_count": subject_count,
        "attendance_count": attendance_count,

        "fee_count": fee_count,
        "paid_fees": paid_fees,
        "partial_fees": partial_fees,
        "unpaid_fees": unpaid_fees,

        "search_query": search_query,
        "selected_class": class_id,
        "filters_applied": bool(search_query or class_id),
    }

    return render(
        request,
        "reports/report_dashboard.html",
        context
    )