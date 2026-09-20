from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from students.models import Student
from .forms import FeeForm
from .models import Fee


@login_required
def fee_dashboard(request):
    fees = Fee.objects.select_related(
        'student',
        'student__user',
        'student__class_name',
        'student__section',
    )

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    if search:
        fees = fees.filter(
            student__student_id__icontains=search
        ) | fees.filter(
            student__user__first_name__icontains=search
        ) | fees.filter(
            student__user__last_name__icontains=search
        )

    if status:
        fees = fees.filter(status=status)

    total_amount = sum(fee.amount for fee in fees)
    total_paid = sum(fee.paid_amount for fee in fees)
    total_due = sum(fee.remaining_amount for fee in fees)

    context = {
        'fees': fees,
        'search': search,
        'selected_status': status,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_due': total_due,
        'student_count': Student.objects.filter(is_active=True).count(),
    }

    return render(request, 'fees/dashboard.html', context)


@login_required
def fee_create(request):
    form = FeeForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Fee record added successfully.')
        return redirect('fee_dashboard')

    return render(
        request,
        'fees/form.html',
        {
            'form': form,
            'title': 'Add Fee Record',
        }
    )


@login_required
def fee_update(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    form = FeeForm(request.POST or None, instance=fee)

    if form.is_valid():
        form.save()
        messages.success(request, 'Fee record updated successfully.')
        return redirect('fee_dashboard')

    return render(
        request,
        'fees/form.html',
        {
            'form': form,
            'title': 'Edit Fee Record',
        }
    )


@login_required
def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)

    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee record deleted successfully.')

    return redirect('fee_dashboard')