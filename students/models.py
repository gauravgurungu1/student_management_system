from django.conf import settings
from django.db import models

from academics.models import AcademicYear, Class, Section


class Guardian(models.Model):
    RELATION_CHOICES = (
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guardian_profile',
    )
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    occupation = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.relation})"


class Student(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
    )

    student_id = models.CharField(
        max_length=20,
        unique=True,
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    address = models.TextField(blank=True)

    phone = models.CharField(
        max_length=15,
        blank=True,
    )

    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='students',
    )

    class_name = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        related_name='students',
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name='students',
    )

    admission_date = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"