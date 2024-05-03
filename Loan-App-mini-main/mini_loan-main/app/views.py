from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


@login_required
def add_repayment(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    scheduled_repayments = Repayment.objects.filter(loan=loan)
    total_remaining_repayments = scheduled_repayments.filter(status='PENDING').count()

    if request.method == 'POST':
        repayment_amount = Decimal(request.POST.get('repayment_amount', '0'))
        Repayment.objects.create(loan=loan, amount=repayment_amount, scheduled_date=timezone.now(), status='PAID')

        if repayment_amount >= loan.amount:
            scheduled_repayments.update(status='PAID')

        
        total_remaining_repayments = scheduled_repayments.filter(status='PENDING').count()
        if total_remaining_repayments == 0:
            loan.state = 'PAID'
            loan.save()

        return redirect('loan_view')

    return render(request, 'app/add_repayment.html', {'loan': loan, 'total_remaining_repayments': total_remaining_repayments})
@staff_member_required
def change_loan_status(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status in ['APPROVED', 'REJECTED']:
            loan.state = new_status
            loan.save()
            return redirect('loan_view')
    return render(request, 'app/change_loan_status.html', {'loan': loan})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('loan_view')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
@login_required
def create_loan(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        term = request.POST['term']
        customer = request.user.customer
        
        
        loan = Loan.objects.create(amount=amount, term=term, customer=customer)
        
        
        return redirect('loan_view')
        
    return render(request, 'app/create_loan.html')

@staff_member_required
def approve_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.state = 'APPROVED'
    loan.save()
    return redirect('loan_view')


@login_required
def view_loans(request):
    user = request.user
    if user.is_staff:  
        loans = Loan.objects.all()  
        return render(request, 'app/admin_view_loans.html', {'loans': loans})
    try:
        customer = user.customer
        loans = Loan.objects.filter(customer=customer)
        return render(request, 'app/view_loans.html', {'loans': loans})
    except User.customer.RelatedObjectDoesNotExist:
        customer = Customer.objects.create(user=user)
        loans = Loan.objects.filter(customer=customer)
        return render(request, 'app/view_loans.html', {'loans': loans})



