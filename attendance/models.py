from django.core.exceptions import ValidationError
from django.db import models

from academics.models import Subject
from students.models import Student


class AttendanceSession(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="attendance_sessions",
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "subject__code"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "date"],
                name="unique_attendance_session_subject_date",
            )
        ]

    def __str__(self):
        return f"{self.subject.code} - {self.date}"


class AttendanceRecord(models.Model):
    PRESENT = "present"
    ABSENT = "absent"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
    ]

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=PRESENT)

    class Meta:
        ordering = ["student__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["session", "student"],
                name="unique_attendance_record_session_student",
            )
        ]

    def clean(self):
        if self.student.course_id != self.session.subject.course_id:
            raise ValidationError("The student must belong to the subject's course.")

    def __str__(self):
        return f"{self.student.name} - {self.session.subject.code} - {self.session.date} - {self.get_status_display()}"
