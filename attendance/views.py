from django.db.models import Case, Count, ExpressionWrapper, F, FloatField, Q, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from academics.models import Course, Subject
from students.models import Student
from .forms import AttendanceRecordForm, AttendanceSessionForm
from .models import AttendanceRecord, AttendanceSession


def attendance_list(request):
    sessions = AttendanceSession.objects.select_related("subject__course").annotate(
        present_count=Count("records", filter=Q(records__status=AttendanceRecord.PRESENT)),
        total_count=Count("records"),
    )
    course_id = request.GET.get("course", "").strip()
    subject_id = request.GET.get("subject", "").strip()
    if course_id.isdigit():
        sessions = sessions.filter(subject__course_id=course_id)
    if subject_id.isdigit():
        sessions = sessions.filter(subject_id=subject_id)
    students = Student.objects.select_related("course").annotate(
        attendance_total=Count("attendance_records"),
        attendance_present=Count(
            "attendance_records",
            filter=Q(attendance_records__status=AttendanceRecord.PRESENT),
        ),
    ).annotate(
        attendance_percentage=Case(
            When(
                attendance_total__gt=0,
                then=ExpressionWrapper(
                    F("attendance_present") * 100.0 / F("attendance_total"),
                    output_field=FloatField(),
                ),
            ),
            default=None,
            output_field=FloatField(null=True),
        ),
    ).order_by("name")
    if course_id.isdigit():
        students = students.filter(course_id=course_id)
    return render(request, "attendance/attendance_list.html", {
        "sessions": sessions,
        "students": students,
        "courses": Course.objects.order_by("name"),
        "subjects": Subject.objects.select_related("course").order_by("course__name", "semester", "code"),
        "selected_course": course_id,
        "selected_subject": subject_id,
    })


def attendance_create(request):
    subject_id = request.POST.get("subject") or request.GET.get("subject")
    course_id = request.POST.get("course") or request.GET.get("course")
    initial = {}
    if subject_id:
        initial["subject"] = subject_id
    if course_id:
        initial["course"] = course_id
    session_form = AttendanceSessionForm(
        request.POST or None,
        course_id=course_id,
        initial=initial,
    )
    subject = None
    if subject_id and str(subject_id).isdigit():
        subject = Subject.objects.select_related("course").filter(pk=subject_id).first()

    if request.method == "POST" and session_form.is_valid():
        subject = session_form.cleaned_data["subject"]
        record_form = AttendanceRecordForm(request.POST, subject=subject)
        if record_form.is_valid():
            session = session_form.save(commit=False)
            session.date = timezone.localdate()
            session.save()
            AttendanceRecord.objects.bulk_create([
                AttendanceRecord(
                    session=session,
                    student_id=student.pk,
                    status=record_form.cleaned_data[f"student_{student.pk}"],
                )
                for student in record_form.students
            ])
            return redirect("attendance_list")
    else:
        record_form = AttendanceRecordForm(subject=subject)
    return render(request, "attendance/attendance_form.html", {
        "session_form": session_form,
        "record_form": record_form,
        "selected_subject": subject,
        "selected_course": course_id,
        "today": timezone.localdate,
        "all_subjects": Subject.objects.select_related("course").order_by(
            "course__name", "semester", "code"
        ),
    })


def attendance_detail(request, id):
    session = get_object_or_404(
        AttendanceSession.objects.select_related("subject__course"), id=id
    )
    records = session.records.select_related("student").all()
    return render(request, "attendance/attendance_detail.html", {
        "session": session,
        "records": records,
        "present_count": records.filter(status=AttendanceRecord.PRESENT).count(),
        "absent_count": records.filter(status=AttendanceRecord.ABSENT).count(),
    })


def student_attendance_history(request, id):
    student = get_object_or_404(Student.objects.select_related("course"), id=id)
    records = AttendanceRecord.objects.filter(student=student).select_related(
        "session__subject"
    )
    total = records.count()
    present = records.filter(status=AttendanceRecord.PRESENT).count()
    percentage = (present / total * 100) if total else None
    return render(request, "attendance/student_history.html", {
        "student": student,
        "records": records,
        "percentage": percentage,
    })
