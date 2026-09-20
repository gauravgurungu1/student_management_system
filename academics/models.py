from django.db import models


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['name']

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=20)
    class_name = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    class Meta:
        unique_together = ('name', 'class_name')
        ordering = ['class_name', 'name']

    def __str__(self):
        return f"{self.class_name.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    class_name = models.ForeignKey(
    Class,
    on_delete=models.CASCADE,
    related_name='subjects',
    null=True,
    blank=True
)
    class Meta:
        ordering = ['class_name', 'name']

    def __str__(self):
        return f"{self.code} - {self.name}"