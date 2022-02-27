from email import message
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from proctoring import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from . tokens import generate_token


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
        email = request.POST.get('email')

        if User.objects.filter(username=username):
            messages.error("User already exist! Please login.")
            return redirect('home')
        if pass1 != pass2:
            messages.eror(request, "Passwords didn't match!")

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = name
        myuser.is_active = False

        myuser.save()

        messages.success(request,"Account successfully created. Please check your email to confirm your email address in order to activate your account.")

        # welcome email

        subject = "Welcome to Automated proctoring platform!"
        message = "Hello"+myuser.first_name + "!!\n"+"Thank you for registering.\n We have also sent you confirmation email, please confirm your email address in order to activate your account.\n\n Thank you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "./html_code/signup.html")

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')



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
