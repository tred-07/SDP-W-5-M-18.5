from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,update_session_auth_hash,authenticate
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from django.contrib import messages 
from . import form

def home(r):
    return render(r,'home.html',{'type':'Home'})

def profile(r):
    if not r.user.is_authenticated:
        return redirect('login')
    return render(r,'profile.html')

def signup(r):
    if r.user.is_authenticated:
        return redirect('profile')
    if r.method=='POST':
       form1=form.SignUp(r.POST)
       if form1.is_valid():
           form1.save()
           messages.success(r,'Sign up Successful')
           return redirect('home')
    return render(r,'form.html',{'form':form.SignUp(),'type':'Sign Up'})


def logIn(r):
    if r.user.is_authenticated:
        return redirect('profile')
    if r.method=='POST':
        form1=AuthenticationForm(request=r,data=r.POST)
        if form1.is_valid():
           name=form1.cleaned_data['username']
           userpassword=form1.cleaned_data['password']
           user=authenticate(username=name,password=userpassword)
           if user is not None:
               login(r,user)
               messages.success(r,'Log in Successful')
               return redirect('profile')
        messages.error(r,'Wrong Credential')
        return render(r,'form.html',{'form':AuthenticationForm(),'type':'Log In'})
    return render(r,'form.html',{'form':AuthenticationForm(),'type':'Log In'})


def logOut(r):
    logout(r)
    messages.success(r,'Log out Successful')
    return redirect('home')


def change_password(r):
    if not r.user.is_authenticated:
        return redirect('login')
    if r.method=='POST':
        form1=PasswordChangeForm(user=r.user,data=r.POST)
        if form1.is_valid():
            form1.save(commit=True)
            update_session_auth_hash(request=r,user=r.user)
            messages.success(r,'Changes Successful')
            return redirect('logout')
        messages.error(r,'Wrong Credential')
        return render(r,'form.html',{'form':form1,'type':'Change Password'})
    else:

        return render(r,'form.html',{'form':PasswordChangeForm(r.POST),'type':'Change Password'})
    

def set_password(r):
    if not r.user.is_authenticated:
        return redirect('login')
    if r.method=='POST':
        form1=SetPasswordForm(user=r.user,data=r.POST)
        if form1.is_valid():
            form1.save()
            messages.success(r,'Changes Successful')
            return redirect('logout')
        messages.error(r,'Wrong Credential')
        return render(r,'form.html',{'form':form1,'type':'Change Password Without Old Password'})
    return render(r,'form.html',{'form':SetPasswordForm(user=r.user),'type':'Change Password Without Old Password'})
    

def edit_profile(r):
    if not r.user.is_authenticated:
        return redirect('login')
    form1=form.EditForm(instance=r.user)
    if r.method=='POST':
        form1=form.EditForm(r.POST,instance=r.user)
        if form1.is_valid():
            form1.save()
            messages.success(r,'Changes Successful')
            return redirect('logout')

    return render(r,'form.html',{'form':form1,'type':'Edit Profile'})
