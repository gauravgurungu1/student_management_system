from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeacherForm
from .models import Teacher


@login_required
def teacher_list(request):

    teachers = Teacher.objects.prefetch_related(
        'subjects'
    ).all()

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    if search_query:

        teachers = teachers.filter(
            full_name__icontains=search_query
        ) | teachers.filter(
            employee_id__icontains=search_query
        ) | teachers.filter(
            email__icontains=search_query
        )

    context = {
        'teachers': teachers,
        'search_query': search_query,
    }

    return render(
        request,
        'teachers/teacher_list.html',
        context
    )


@login_required
def teacher_add(request):

    if request.method == 'POST':

        form = TeacherForm(
            request.POST
        )

        if form.is_valid():

            teacher = form.save()

            messages.success(
                request,
                'Teacher added successfully.'
            )

            return redirect(
                'teacher_list'
            )

    else:

        form = TeacherForm()

    context = {
        'form': form,
        'page_title': 'Add Teacher',
        'button_text': 'Add Teacher',
    }

    return render(
        request,
        'teachers/teacher_form.html',
        context
    )


@login_required
def teacher_edit(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == 'POST':

        form = TeacherForm(
            request.POST,
            instance=teacher
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Teacher updated successfully.'
            )

            return redirect(
                'teacher_list'
            )

    else:

        form = TeacherForm(
            instance=teacher
        )

    context = {
        'form': form,
        'teacher': teacher,
        'page_title': 'Edit Teacher',
        'button_text': 'Update Teacher',
    }

    return render(
        request,
        'teachers/teacher_form.html',
        context
    )


@login_required
def teacher_delete(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == 'POST':

        teacher.delete()

        messages.success(
            request,
            'Teacher deleted successfully.'
        )

        return redirect(
            'teacher_list'
        )

    context = {
        'teacher': teacher,
    }

    return render(
        request,
        'teachers/teacher_confirm_delete.html',
        context
    )