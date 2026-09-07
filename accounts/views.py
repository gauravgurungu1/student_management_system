from django.shortcuts import render
from students.models import Student
from academics.models import Course
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


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

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    students = Student.objects.all()
    total_students = Student.objects.count()
    total_course = Course.objects.count()

    return render(request, 'dashboard.html', {
        'students': students,
        'total_students': total_students,
        'total_course' : total_course,
    })
    return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')
