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

from . import viewsroommates
# Create your views here.

# ===========================
# ======  Display ===========
# ===========================

# All Bills listed by date submitted
@login_required(login_url="/login/")
def index(request):
    all_bills = Bills.objects.all().order_by('-date')
    context = {
        'sitename':"RoomateBills",
        'page_name':"Bills",
        'all_bills':all_bills,
    }
    return render(request, 'bills.html', context)

# All Bills Organized by Month
@login_required(login_url="/login/")
def indexbymonth(request):
    month_bills = BillingMonth.objects.all()
    month_bills = month_bills.order_by('-theyear', '-themonthnum')
    web_info    = homeMOTD.objects.get(pk=1)
    all_roommates = Roommates.objects.all()
    context = {
        'sitename':"RoomateBills",
        'page_name':"Bills",
        'month_bills':month_bills,
        'web_info':web_info,
    }
    return render(request, 'billsbymonth.html', context)

# Details of a single Bill
@login_required(login_url="/login/")
def viewBill(request, bill_id):
    bill = Bills.objects.get(pk=bill_id)
    month = bill.month
    context = {
        'bill':bill,
        'month':month,
    }
    return render(request, 'billdetails.html', context)

# ===========================
# ===== Create/Submit  ======
# ===========================

@login_required(login_url="/login/")
def submitBill(request):
    if request.method=='POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request, commit=False)
            j.save()
            BillingMonth.objects.get(pk=j.month.id).addbill(instance=j.id, cat=j.category)
            return HttpResponseRedirect('/bills/bymonth')
    else:
        form = RecipeForm()
    context = {
        'sitename':"EdgarRaw",
        'page_name':"Add a Bill - EdgarRaw",
        'form':form,
    }
    return render(request, 'addbill.html', context)

# ===========================
# ========  Edit  ===========
# ===========================

@login_required(login_url="/login/")
def editBill(request, bill_id):
    post = Bills.objects.get(pk=bill_id)
    thefile = post.image
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.update(instance=bill_id, thefile=thefile, commit=False)
            post.save()
            context = {
                'bill':post,
            }
            return render(request, 'billDetails.html', context)
    else:
        form = RecipeForm(instance=post)
    context = {
        'post':post,
        'form':form,
    }
    return render(request, 'editbill.html', context)

# ===========================
# ======== Delete ===========
# ===========================

@login_required(login_url="/login/")
def deletebill(request, bill_id):
    bill = Bills.objects.get(pk=bill_id)
    month = bill.month.id
    bill.delete()
    BillingMonth.objects.get(pk=bill.month.id).addbill(instance=0, cat="none")
    return HttpResponseRedirect("/bills/")
