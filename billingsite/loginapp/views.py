from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.http import JsonResponse
import datetime
from django.contrib.auth.decorators import login_required

import json as json

from .forms import *

from django.contrib.auth import authenticate, login
# Create your views here.
#@login_required(login_url="/login/")
def index(request):
    #formname=LoginForm.username()
    #formpass=LoginForm.password()
    form = LoginForm()
    context = {
        'sitename':"EdgarRaw",
        'page_name':"Log In",
        'form':form,
    }
    return render(request, 'login.html', context)

def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            print(login(request, user))
            return HttpResponseRedirect('/')

    else:
        form = RegisterForm
        print("something")
        # form = blog_entry()
    context = {
        'page_name':"Register",
        'form':form,
    }
    return render(request, 'register.html', context)
