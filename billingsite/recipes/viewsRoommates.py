from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.http import JsonResponse
import datetime
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Q

import json as json
from .forms import RecipeForm, MonthForm
from .models import Bills, BillingMonth
from loginapp.models import Payments, Roommates, homeMOTD
from loginapp.forms import PaymentForm, RoommatesForm

# Create your views here.

# ===========================
# ======  Display ===========
# ===========================

@login_required(login_url="/login/")
def allroommates(request):
    roommates = Roommates.objects.all()
    payments  = Payments.objects.all().order_by('datepaid')
    tempmate  = Roommates.objects.get(pk=1)
    tempmate.recalcOwed()
    context = {
        'roommates':roommates,
        'payments':payments,
    }
    return render(request, 'allroommates.html', context)

@login_required(login_url="/login/")
def userpayments(request, roommate_id):
    roommate = Roommates.objects.get(pk=roommate_id)
    item = Payments.objects.all()
    context = {
        'payments':item,
        'roommate':roommate,
    }
    return render(request, 'userpayments.html', context)

@login_required(login_url="/login/")
def paymentdetails(request, payment_id):
    item = Payments.objects.get(pk=payment_id)
    context = {
        'item':item,
    }
    return render(request, 'paymentDetails.html', context)


# ===========================
# ===== Create/Submit  ======
# ===========================

@login_required(login_url="/login/")
def submitPayment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST);
        if form.is_valid():
            j = form.save()
            j.save
            roommate = Roommates.objects.filter(id=j.roommate.id)
            roommate.update()
            return HttpResponseRedirect('/bills/submitpayment/')
    else:
        form = PaymentForm();
    context = {
        'form':form,
    }
    return render(request, 'addpayment.html', context)

@login_required(login_url="/login/")
def submitPaymentFor(request, roommate_id):
    roomy= Roommates.objects.get(pk=roommate_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST);
        if form.is_valid():
            j = form.save()
            j.save
            roommate = Roommates.objects.filter(id=j.roommate.id)
            roommate.update()
            return HttpResponseRedirect('/bills/submitpayment/')
    else:
        form = PaymentForm();
    context = {
        'roomy':roomy,
        'form':form,
    }
    return render(request, 'addpayment.html', context)

# ===========================
# ========  Edit  ===========
# ===========================

@login_required(login_url="/login/")
def edituserpayments(request, payment_id, roommate_id):
    payment = Payments.objects.get(pk=payment_id)
    roommate = Roommates.objects.get(pk=roommate_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            context = {
                'payments':payment,
                'roommate':roommate,
                'form':form,
            }
            return render(request, 'editpayment.html', context)
    else:
        form = RecipeForm(instance=payment)
    context = {
        'payments':payment,
        'roommate':roommate,
        'form':form,
    }
    return render(request, 'editpayment.html', context)

@login_required(login_url="/login/")
def editroommate(request, roommate_id):
    roommate = Roommates.objects.get(pk=roommate_id)
    if request.method == "POST":
        form = RoommatesForm(request.POST, instance=roommate)
        if form.is_valid():
            j = form.save(commit=False)
            j.comment(form)
            return HttpResponseRedirect('/bills/allroommates/')
    else:
        form = RoommatesForm(instance=roommate)
    context = {
        'roommate':roommate,
        'form':form,
    }
    return render(request, 'editroommate.html', context)


# ===========================
# ======== Delete ===========
# ===========================

@login_required(login_url="/login/")
def deletepayment(request, payment_id):
    payment = Payments.objects.get(pk=payment_id)
    roommate_id = Payments.objects.get(pk=payment_id).roommate.id
    payment.delete()
    Roommates.objects.get(id=roommate_id).update()
    return HttpResponseRedirect("/bills/roommate/%s/" % roommate_id)
