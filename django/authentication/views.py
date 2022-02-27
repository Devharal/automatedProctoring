from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, "./html_code/homepage/index.html")

def stuindex(request):
    return render(request, "./html_code/indexes/stuindex.html")
    

def signup(request):

    if request.method == "POST":
        username = request.POST.get('email')
        name = request.POST.get('name')
        pass1 = request.POST.get('pass')
        pass2 = request.POST.get('re_pass')

        myuser = User.objects.create_user(username,pass1)
        myuser.first_name = name

        myuser.save()

        messages.success(request,"successfully created")

        return redirect('signin')

    return render(request, "./html_code/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST.get("email")
        pass1 = request.POST.get('your_pass')

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request,user)
            name = user.first_name
            return render(request, "./html_code/indexes/stuindex.html",{'name':name})
        else:
            messages.error(request, "Bad credentials")
            return redirect("home")



    return render(request, "./html_code/Login.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully! ")
    return redirect('home')
