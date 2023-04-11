from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.conf import settings
from .models import User

def signup_view(request):
    if request.method == "GET":
        return render(request,'html/sigup.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.get(username=username)
            messages.error(request,'username already used')
        except User.DoesNotExist:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            login(request,user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return redirect('auth:signup')

def login_view(request):
    if request.method == "GET":
        return render(request,'html/login.html')
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        messages.error(request,'Invalid credentials')
        return render(request,'html/login.html')
