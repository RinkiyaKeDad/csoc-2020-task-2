from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def loginView(request):
    if request.method == 'GET':
        return render(request,'authentication/loginUser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'authentication/loginUser.html',{'form':AuthenticationForm(),'error':'Username and Password did not match.'})
        else:
            login(request,user)
            return redirect('index')
    

def logoutView(request):
    logout(request)
    return redirect('index')

def registerView(request):
    if request.method == 'GET':
        return render(request,'authentication/registerUser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('index')

            except IntegrityError:
                return render(request,'authentication/registerUser.html',{'form':UserCreationForm(),'error':'Username Already Taken. Try Again'})               

        else:
            return render(request,'authentication/registerUser.html',{'form':UserCreationForm(),'error':'Passwords Did Not Match. Try Again.'})


