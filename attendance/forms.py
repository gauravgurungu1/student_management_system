from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from academics.models import Course, Subject
from students.models import Student
from .models import AttendanceRecord, AttendanceSession


class AttendanceSessionForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.order_by("name"),
        required=True,
        empty_label="Select a course",
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-3 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500",
        }),
    )

    class Meta:
        model = AttendanceSession
        fields = ["subject"]
        widgets = {
            "subject": forms.Select(attrs={
                "class": "w-full px-4 py-3 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500",
            }),
        }

    def __init__(self, *args, course_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.none()
        self.fields["subject"].label_from_instance = lambda subject: (
            f"Semester {subject.semester} - {subject.code} - {subject.name}"
        )
        selected_course_id = course_id
        if not selected_course_id and self.data:
            selected_course_id = self.data.get("course")
        if not selected_course_id and self.initial.get("course"):
            selected_course_id = self.initial["course"]
        if str(selected_course_id).isdigit():
            self.fields["course"].initial = selected_course_id
            self.fields["subject"].queryset = Subject.objects.filter(
                course_id=selected_course_id
            ).order_by("semester", "code")

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get("course")
        subject = cleaned_data.get("subject")
        if course and subject and subject.course_id != course.pk:
            raise ValidationError("The selected subject does not belong to the selected course.")
        if subject and AttendanceSession.objects.filter(
            subject=subject, date=timezone.localdate()
        ).exists():
            raise ValidationError(
                "Today's attendance for this subject already exists. View the existing session."
            )
        return cleaned_data

class AttendanceRecordForm(forms.Form):
    def __init__(self, *args, subject=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.students = Student.objects.none()
        if subject:
            self.students = Student.objects.filter(course=subject.course).order_by("name")
            for student in self.students:
                self.fields[f"student_{student.pk}"] = forms.ChoiceField(
                    label=student.name,
                    choices=AttendanceRecord.STATUS_CHOICES,
                    initial=AttendanceRecord.PRESENT,
                    widget=forms.RadioSelect,
                )
