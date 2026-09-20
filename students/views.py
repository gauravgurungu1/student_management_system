from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


@login_required
def student_list(request):
    students = Student.objects.select_related(
        'user',
        'academic_year',
        'class_name',
        'section',
    ).order_by('student_id')

    search = request.GET.get('search', '').strip()

    if search:
        students = students.filter(
            student_id__icontains=search
        ) | students.filter(
            user__first_name__icontains=search
        ) | students.filter(
            user__last_name__icontains=search
        )

    return render(request, 'students/student_list.html', {
        'students': students,
        'search': search,
    })


@login_required
def student_create(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add Student',
    })


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    form = StudentForm(
        request.POST or None,
        instance=student
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_list')

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Edit Student',
    })


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        if student.user:
            student.user.delete()
        else:
            student.delete()

        messages.success(request, 'Student deleted successfully.')

    return redirect('student_list')