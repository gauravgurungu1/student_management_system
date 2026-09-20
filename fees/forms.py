from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = [
            'student',
            'fee_type',
            'amount',
            'paid_amount',
            'due_date',
            'description',
        ]

        widgets = {
            'due_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Optional description'
                }
            ),
        }