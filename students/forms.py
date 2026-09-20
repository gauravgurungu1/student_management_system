from django import forms
from django.contrib.auth.models import User

from .models import Student, Guardian


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Student
        fields = [
            'student_id',
            'date_of_birth',
            'gender',
            'address',
            'phone',
            'guardian',
            'academic_year',
            'class_name',
            'section',
            'is_active',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def save(self, commit=True):
        student = super().save(commit=False)

        if not student.user_id:
            user = User.objects.create_user(
                username=self.cleaned_data['student_id'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
            )
            student.user = user
        else:
            user = student.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()

        if commit:
            student.save()

        return student