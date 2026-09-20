from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from academics.models import AcademicYear, Class, Section, Subject
from students.models import Student


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'active_student_count': Student.objects.filter(
            is_active=True
        ).count(),
        'academic_year_count': AcademicYear.objects.count(),
        'class_count': Class.objects.count(),
        'section_count': Section.objects.count(),
        'subject_count': Subject.objects.count(),
    }

    return render(
        request,
        'dashboard.html',
        context
    )