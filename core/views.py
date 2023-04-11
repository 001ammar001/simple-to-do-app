from time import strptime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import decorators,logout
from django.contrib import messages
from django.conf import settings
from .models import Task
from datetime import datetime

    
def logout_view(request):
    if request.user is not None:
        logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

@decorators.login_required()
def main_view(request):
    if request.method=="GET":
        tasks = Task.objects.filter(user=request.user,status='pending',date__gte=datetime.now()).order_by('date')
        return render(request,'html/main.html',{'tasks':tasks,'view':'main'})

@decorators.login_required()
def succsess_tasks_view(request):
    if request.method=="GET":
        tasks = Task.objects.filter(user=request.user,status='sucsess').order_by('date')
        return render(request,'html/main.html',{'tasks':tasks,'view':'succsess-tasks'})

@decorators.login_required()   
def archived_tasks_view(request):
    if request.method=="GET":
        tasks = Task.objects.filter(user=request.user,status='archived').order_by('date')
        return render(request,'html/main.html',{'tasks':tasks,'view':'archived-tasks'})

@decorators.login_required()
def overdue_tasks_view(request):
    if request.method=="GET":
        tasks = Task.objects.filter(user=request.user,status='pending',date__lte=datetime.now()).order_by('date')
        return render(request,'html/main.html',{'tasks':tasks,'view':'overdue-tasks'})

@decorators.login_required()
def change_task_view(request,id):
    if request.method == 'POST':
        action = request.POST.get('action')
        print(action)
        task = get_object_or_404(Task,id=id)
        action , view = action.split('-!-')
        if action == 'delete':
            task.delete()
            messages.success(request,'task deleted sucessfully')

        elif action == 'archive':
            task.status = 'archived'
            task.save()
            messages.success(request,'task archived sucessfully')

        elif action == 'sucsess':
            task.status = 'sucsess'
            task.save()
            messages.success(request,'task combleted sucessfully')

        return redirect(f'core:{view}')
    return redirect('core:main')

@decorators.login_required()
def add_task_view(request):
    
    if request.method == "GET":
        return render(request,"html/add_task.html")
    if request.method == "POST":
        title = request.POST.get("title").lstrip()
        body = request.POST.get("body").lstrip()
        date = request.POST.get("date")
        now = datetime.now()

        try:
            date = strptime(date,f"%Y-%m-%dT%H:%M")
            date = datetime(date.tm_year,date.tm_mon,date.tm_mday,date.tm_hour,date.tm_min)

            if body == '' or title == '' or date == '':
                messages.error(request,'please enter all the data')

            elif now > date:
                messages.error(request,'task date must be at the present')

            else:
                Task.objects.create(user=request.user,title=title,body=body,date=date)   
                messages.success(request,'Task added successfully')
        
        except ValueError:
            messages.error(request,'time format error , year must be less than 9999')
  
        return render(request,'html/add_task.html')
    
