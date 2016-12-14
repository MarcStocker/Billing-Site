from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.http import JsonResponse
import datetime, random
from django.contrib.auth.decorators import login_required



import json as json
from .models import TodoList
from loginapp.models import edgar, Roommates, Payments
from loginapp.forms import EdgarForm
from recipes.models import Bills, BillingMonth

from .forms import AuthenticationForm, LoginForm
# Create your views here.
#@login_required(login_url="/home/")
def home(request):
    month_bills = BillingMonth.objects.all()
    month_bills = month_bills.order_by('-theyear', '-themonthnum')
    all_roommates = Roommates.objects.all()
    context = {
        'sitename':"RoomateBills",
        'page_name':"Bills",
        'month_bills':month_bills,
    }
    return render(request, 'billsbymonth.html', context)

# Old homepage... maybe I'll keep it and edit it later
# def home(request):
#     # grab the max id in the database
#     all_bills = Bills.objects.all()
#
#     webinfo = edgar.objects.filter(id__gte=1)[0]
#     context = {
#         'sitename':"720 Bills",
#         'page_name':"Home - Bills",
#         'all_bills':all_bills,
#         'webinfo': webinfo,
#     }
#     return render(request, 'billsbymonth.html', context)

def editwebsite(request):
    webinfo = edgar.objects.filter(id__gte=1)[0]
    if request.method=='POST':
        form = EdgarForm(request.POST, request.FILES, instance=webinfo)
        if form.is_valid():
            webinfo = form.save(commit=False)
            webinfo.save()
            return HttpResponseRedirect("/home/")
    else:
        form = EdgarForm(instance=webinfo)
    context = {
        'webinfo':webinfo,
        'form':form,
    }
    return render(request, 'editwebsite.html', context)
