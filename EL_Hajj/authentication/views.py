from django.shortcuts import render, redirect
from django.contrib import messages
from .models import elHadj
from rest_framework. response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import elHadj
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



def send_activation_email(user, request):
    current_site = get_current_site(request).domain
    email_subject = 'Activate your account'
    email_body = render_to_string('/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    
    EmailThread(email).start()




def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        password = request.POST.get('password')
        dateOfBirth = request.POST.get('dateOfBirth')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        province = request.POST.get('province')
        gender = request.POST.get('gender')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 6 characters')
            context['has_error'] = True

            return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/register.html', context, status=409)

        if context['has_error']:
            return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/register.html', context)

        user = elHadj.objects.create_user(email=email, password=password,dateOfBirth=dateOfBirth,last_name=last_name,first_name=first_name,gender=gender,
                                          city=city,province=province,phone=phone)
        user.set_password(password)
        user.save()

        if not context['has_error']:

            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')
            return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/login.html')

    return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/register.html')



def login_user(request):

    if request.method == 'POST':
        context = {'data': request.POST}
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = get_object_or_404(elHadj,email = email)
        if not user.check_password(password):
            return render(request,'/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/activate-s.html',status=status.HTTP_400_BAD_REQUEST)
        
        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox')
            return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/login.html', context, status=401)
        
        
        return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/home.html')

    return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/login.html')


def logout_user(request):

    logout(request)

    return redirect (reverse('login'))


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = elHadj.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/activate-s.html', {"user": user})
    
    return render(request, '/Users/mac/ELHADJ/back-end/EL_Hajj/authentication/templates/activate-failed.html', {"user": user})



def email_existance_verification(request):
    email = get_object_or_404(elHadj,email = request.data['email'])
    if email :
        return Response({'error':'Email already exists'},status=status.HTTP_400_BAD_REQUEST)
