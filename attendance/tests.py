from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academics.models import Course, Subject
from students.models import Student
from .models import AttendanceRecord, AttendanceSession


class AttendanceTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Computer Science", code="CS", duration_years=4)
        self.other_course = Course.objects.create(name="Business", code="BUS", duration_years=4)
        self.subject = Subject.objects.create(
            course=self.course, name="Programming", code="CS101", semester=1, credit_hours=3
        )
        self.student = Student.objects.create(
            name="Test Student", email="student@example.com", phone="9800000000", course=self.course
        )
        self.other_student = Student.objects.create(
            name="Business Student", email="business@example.com", phone="9800000001", course=self.other_course
        )

    def test_session_and_bulk_records_can_be_created(self):
        response = self.client.post(reverse("attendance_create"), {
            "course": self.course.pk,
            "subject": self.subject.pk,
            "date": "2026-09-11",
            f"student_{self.student.pk}": AttendanceRecord.PRESENT,
        })
        self.assertRedirects(response, reverse("attendance_list"))
        self.assertEqual(AttendanceSession.objects.count(), 1)
        self.assertEqual(AttendanceRecord.objects.count(), 1)

    def test_duplicate_session_is_rejected(self):
        AttendanceSession.objects.create(subject=self.subject, date=timezone.localdate())
        response = self.client.post(reverse("attendance_create"), {
            "course": self.course.pk,
            "subject": self.subject.pk,
            "date": "2026-09-11",
            f"student_{self.student.pk}": AttendanceRecord.PRESENT,
        })
        self.assertContains(response, "already exists", status_code=200)
        self.assertEqual(AttendanceSession.objects.count(), 1)

    def test_record_rejects_student_from_wrong_course(self):
        session = AttendanceSession.objects.create(subject=self.subject, date=date(2026, 9, 11))
        record = AttendanceRecord(session=session, student=self.other_student, status=AttendanceRecord.PRESENT)
        with self.assertRaises(ValidationError):
            record.full_clean()

    def test_student_overall_percentage_uses_all_records(self):
        first = AttendanceSession.objects.create(subject=self.subject, date=date(2026, 9, 10))
        second = AttendanceSession.objects.create(subject=self.subject, date=date(2026, 9, 11))
        AttendanceRecord.objects.create(session=first, student=self.student, status=AttendanceRecord.PRESENT)
        AttendanceRecord.objects.create(session=second, student=self.student, status=AttendanceRecord.ABSENT)
        response = self.client.get(reverse("student_attendance_history", args=[self.student.pk]))
        self.assertContains(response, "50.0%")
