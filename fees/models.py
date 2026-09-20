from django.db import models
from students.models import Student


class Fee(models.Model):
    FEE_TYPE_CHOICES = (
        ('admission', 'Admission Fee'),
        ('tuition', 'Tuition Fee'),
        ('exam', 'Exam Fee'),
        ('library', 'Library Fee'),
        ('transport', 'Transport Fee'),
        ('other', 'Other Fee'),
    )

    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('unpaid', 'Unpaid'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fees'
    )
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    due_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='unpaid'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.paid_amount >= self.amount:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'partial'
        else:
            self.status = 'unpaid'

        super().save(*args, **kwargs)

    @property
    def remaining_amount(self):
        return self.amount - self.paid_amount

    def __str__(self):
        return f"{self.student.student_id} - {self.fee_type}"