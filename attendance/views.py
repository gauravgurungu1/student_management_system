from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from academics.models import Class, Section
from students.models import Student

from .models import Attendance


@login_required
def attendance_dashboard(request):

    selected_date = request.GET.get(
        'date',
        date.today().isoformat()
    )

    selected_class = request.GET.get('class')
    selected_section = request.GET.get('section')

    classes = Class.objects.all()
    sections = Section.objects.all()

    students = []

    if selected_class and selected_section:

        student_queryset = Student.objects.filter(
            is_active=True,
            class_name_id=selected_class,
            section_id=selected_section
        ).select_related(
            'user',
            'class_name',
            'section'
        ).order_by('student_id')

        for student in student_queryset:

            attendance = Attendance.objects.filter(
                student=student,
                date=selected_date
            ).first()

            student.attendance_record = attendance

            students.append(student)

    context = {
        'classes': classes,
        'sections': sections,
        'students': students,
        'selected_date': selected_date,
        'selected_class': selected_class,
        'selected_section': selected_section,
    }

    return render(
        request,
        'attendance/dashboard.html',
        context
    )


@login_required
@transaction.atomic
def save_attendance(request):

    if request.method != 'POST':
        return redirect('attendance_dashboard')

    attendance_date = request.POST.get('date')
    class_id = request.POST.get('class_id')
    section_id = request.POST.get('section_id')

    if not attendance_date or not class_id or not section_id:

        messages.error(
            request,
            'Date, class and section are required.'
        )

        return redirect('attendance_dashboard')

    students = Student.objects.filter(
        is_active=True,
        class_name_id=class_id,
        section_id=section_id
    )

    for student in students:

        status = request.POST.get(
            f'status_{student.id}'
        )

        remarks = request.POST.get(
            f'remarks_{student.id}',
            ''
        ).strip()

        if status:

            Attendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                defaults={
                    'status': status,
                    'remarks': remarks,
                    'marked_by': request.user,
                }
            )

    messages.success(
        request,
        'Attendance saved successfully.'
    )

    return redirect(
        f'/attendance/?date={attendance_date}'
        f'&class={class_id}'
        f'&section={section_id}'
    )


@login_required
def attendance_history(request):

    records = Attendance.objects.select_related(
        'student',
        'student__user',
        'student__class_name',
        'student__section'
    ).all()

    selected_date = request.GET.get('date')
    selected_class = request.GET.get('class')
    selected_section = request.GET.get('section')
    selected_status = request.GET.get('status')

    if selected_date:
        records = records.filter(
            date=selected_date
        )

    if selected_class:
        records = records.filter(
            student__class_name_id=selected_class
        )

    if selected_section:
        records = records.filter(
            student__section_id=selected_section
        )

    if selected_status:
        records = records.filter(
            status=selected_status
        )

    context = {
        'records': records,
        'classes': Class.objects.all(),
        'sections': Section.objects.all(),
        'selected_date': selected_date,
        'selected_class': selected_class,
        'selected_section': selected_section,
        'selected_status': selected_status,
    }

    return render(
        request,
        'attendance/history.html',
        context
    )