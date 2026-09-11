from django import forms

from .models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher

        fields = [
            'employee_id',
            'full_name',
            'email',
            'phone',
            'qualification',
            'address',
            'hire_date',
            'subjects',
            'is_active',
        ]

        widgets = {
            'employee_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. TCH001',
                }
            ),

            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter teacher name',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'teacher@example.com',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone number',
                }
            ),

            'qualification': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. M.Sc. CSIT',
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter address',
                    'rows': 3,
                }
            ),

            'hire_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'subjects': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-checkbox',
                }
            ),
        }