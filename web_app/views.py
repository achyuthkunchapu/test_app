from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Work
from .forms import SignUpForm
from django.contrib.auth import login
from .resources import WorkResource
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from tablib import  Dataset
from django.contrib.auth import authenticate, login
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
import random
import cx_Oracle
import pandas as pd
import json
import csv
from django.http import JsonResponse
from prettytable import PrettyTable
from IPython.display import HTML
import openpyxl
import os
import mimetypes


# Create your views here.
@login_required
def index(request):
    try:
        if request.method =='POST':

            work_resource = WorkResource()
            dataset = Dataset()
            new_work = request.FILES['myfile']
            if new_work.name.lower().endswith('.csv'):

                 imported_data = dataset.load(new_work.read().decode('utf-8'),format='csv')

            else:

                 imported_data = dataset.load(new_work.read(),format='xlsx')
            for data in imported_data:

                value = Work(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
                )
                value.save()
            messages.success(request,'Upload Success !')

        return render(request,'index.html')
    except :
        messages.warning(request,'Upload Failed - Make Sure to Upload Correct File')
        return render(request,'index.html')



@login_required
def home(request):
    return render(request,'home.html')

@login_required
def main(request):
    return render(request,'main.html')


@login_required
def newsetup(request):
    return render(request,'newsetup.html')

@login_required
def schemecategorymapping(request):
    return render(request,'schemecategorymapping.html')


@login_required
def read(request):
    query_results = Work.objects.all()
    return render(request,'read.html',{'query_results':query_results})


@login_required
def download(request):
     try:
            output = []
            response = HttpResponse (content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="LNTpoc.csv"'
            writer = csv.writer(response)
            query_set = Work.objects.all()
            #Header
            fields=['id','key','Issue_Type','Summary','Status','Application']

            writer.writerow(fields)
            for item in query_set:
                output.append([item.id, item.key, item.Issue_Type, item.Summary,item.Status,item.Application])
            #CSV Data
            writer.writerows(output)
            return response


     except cx_Oracle.Error as error:
                messages.warning(request,'Download Failed: ', error)
                return responsee


def register(request):
	if request.method == 'POST':
		get_otp = request.POST.get('otp')

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				messages.success(request, f'Account is Created For {usr.username}')
				return redirect('login')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'register.html', {'otp': True, 'usr': usr})

		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')


			usr = User.objects.get(username=username)
			#usr.email = email

			usr.is_active = False
			usr.save()
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)

			mess = f"Your OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to LnT POC - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)

			return render(request, 'register.html', {'otp': True, 'usr': usr})


	else:
		form = SignUpForm()

	return render(request, 'register.html', {'form':form})

def login_view(request):
    #if request.user.is_authenticated:
    #    return redirect('home')
    if request.method == 'POST':
        usrname = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username = usrname, password = passwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        elif not User.objects.filter(username = usrname).exists():
            messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')
        else:
            messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')
    form = AuthenticationForm()
    return render(request,'login.html',{'form': form})
