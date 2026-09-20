from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import AcademicYear, Class, Section, Subject
from .forms import (
    AcademicYearForm,
    ClassForm,
    SectionForm,
    SubjectForm,
)


@login_required
def academics_dashboard(request):
    context = {
        'academic_years': AcademicYear.objects.all(),
        'classes': Class.objects.all(),
        'sections': Section.objects.select_related('class_name').all(),
        'subjects': Subject.objects.select_related('class_name').all(),
    }

    return render(request, 'academics/dashboard.html', context)


@login_required
def academic_year_create(request):
    form = AcademicYearForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Academic year created successfully.')
        return redirect('academics_dashboard')

    return render(request, 'academics/form.html', {
        'form': form,
        'title': 'Add Academic Year',
    })


@login_required
def class_create(request):
    form = ClassForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Class created successfully.')
        return redirect('academics_dashboard')

    return render(request, 'academics/form.html', {
        'form': form,
        'title': 'Add Class',
    })


@login_required
def section_create(request):
    form = SectionForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Section created successfully.')
        return redirect('academics_dashboard')

    return render(request, 'academics/form.html', {
        'form': form,
        'title': 'Add Section',
    })


@login_required
def subject_create(request):
    form = SubjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Subject created successfully.')
        return redirect('academics_dashboard')

    return render(request, 'academics/form.html', {
        'form': form,
        'title': 'Add Subject',
    })


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')

    return redirect('academics_dashboard')