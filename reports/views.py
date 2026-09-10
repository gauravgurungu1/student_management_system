from django.db.models import Count, Q
from django.shortcuts import render

from academics.models import Course, Subject
from students.models import Student


def report_dashboard(request):
    """
    Reports dashboard with summary statistics,
    course-wise student counts, and student filters.
    """

    # Get filter values from the request
    search_query = request.GET.get("search", "").strip()
    course_id = request.GET.get("course", "").strip()

    # Base student queryset
    students = Student.objects.select_related("course").all()

    # Search by student name or email
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    # Filter by course
    if course_id.isdigit():
        students = students.filter(course_id=course_id)
    elif course_id:
        course_id = ""

    # Keep results predictable
    students = students.order_by("name")

    # Summary data
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_subjects = Subject.objects.count()

    # Course-wise student summary
    course_summary = (
        Course.objects
        .annotate(student_count=Count("students"))
        .order_by("name")
    )

    context = {
        "students": students,
        "courses": Course.objects.order_by("name"),
        "course_summary": course_summary,

        "total_students": total_students,
        "total_courses": total_courses,
        "total_subjects": total_subjects,

        "search_query": search_query,
        "selected_course": course_id,
        "filters_applied": bool(search_query or course_id),
    }

    return render(request, "reports/report_dashboard.html", context)