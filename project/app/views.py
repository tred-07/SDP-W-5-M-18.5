from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from . import form

def signup(r):
    if r.user.is_authenticated:
        return HttpResponse('profile')
    form1=form.SignUp()
    return render(r,'form.html',{'form':form1})