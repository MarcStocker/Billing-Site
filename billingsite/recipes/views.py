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

def index(request):
    all_bills = Bills.objects.all().order_by('-date')
    context = {
        'sitename':"RoomateBills",
        'page_name':"Bills",
        'all_bills':all_bills,
    }
    return render(request, 'bills.html', context)

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

@login_required(login_url="/login/")
def viewBill(request, bill_id):
    bill = Bills.objects.get(pk=bill_id)
    month = bill.month
    context = {
        'bill':bill,
        'month':month,
    }
    return render(request, 'billdetails.html', context)

@login_required(login_url="/login/")
def paymentdetails(request, payment_id):
    item = Payments.objects.get(pk=payment_id)
    context = {
        'item':item,
    }
    return render(request, 'paymentDetails.html', context)

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
def deletebill(request, bill_id):
    bill = Bills.objects.get(pk=bill_id)
    month = bill.month.id
    bill.delete()
    BillingMonth.objects.get(pk=bill.month.id).addbill(instance=0, cat="none")
    return HttpResponseRedirect("/bills/")

@login_required(login_url="/login/")
def deletepayment(request, payment_id):
    payment = Payments.objects.get(pk=payment_id)
    roommate_id = Payments.objects.get(pk=payment_id).roommate.id
    payment.delete()
    Roommates.objects.get(id=roommate_id).update()
    return HttpResponseRedirect("/bills/roommate/%s/" % roommate_id)

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

# def editpayment(request, payment_id):
#     payment = Payments.objects.get(pk=payment_id)
#     if request.method == "POST":
#         form = RecipeForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.update(instance=recipe_id, thefile=thefile, commit=False)
#             post.save()
#             context = {
#                 'bill':post,
#             }
#             return render(request, 'billDetails.html', context)
#     else:
#         form = RecipeForm(instance=post)
#     context = {
#         'post':post,
#         'form':form,
#     }
#     return render(request, 'editbill.html', context)

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
def allroommates(request):
    roommates = Roommates.objects.all()
    payments  = Payments.objects.all().order_by('datepaid')
    context = {
        'roommates':roommates,
        'payments':payments,
    }
    return render(request, 'allroommates.html', context)
