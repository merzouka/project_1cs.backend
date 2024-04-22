from random import randint, random
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.contrib.auth.hashers import make_password
from authentication.serializers import userSerializer
from .models import PasswordReset, user
from rest_framework import status
from django.shortcuts import get_object_or_404,render

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.contrib.auth import logout, login ,get_user_model,authenticate
from django.urls import reverse 
from django.views.decorators.csrf import csrf_exempt


@api_view(["POST"])
@parser_classes([JSONParser])
def send_verification_email(request):
    email = request.data["email"]
    # email attached to account
    try:
        user_: user = user.objects.get(email=email)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

    code = randint(0, 9999)
    try:
        send_mail(
            "Email de confirmation",
            f"Bienvenue sur le site Web El Hajj,\n votre code de confirmation est {code}",
            "celeq.elhajj@gmail.com",
            [email]
        )
        user_.code = f"{code}"
        user_.save()
        return Response(JSONRenderer().render({ "message": "email sent" }), 200)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

@api_view(["POST"])
@parser_classes([JSONParser])
def verify_email(request):
    email = request.data["email"]
    code = request.data["code"]
    
    user = get_user_model()
    
    try:
        user = user.objects.get(email=email,code=code)
    except user.DoesNotExist:
        return Response(JSONRenderer().render({ "message": "invalid address or code" }), 400)
    user.is_email_verified = True 
    user.save()
    return Response(JSONRenderer().render({ "message": "Email verified" }), 200)
    
@csrf_exempt    
@api_view(['GET', 'POST'])
def register(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    dateOfBirth = data.get('dateOfBirth')
    city = data.get('city')
    province = data.get('province')
    gender = data.get('gender')
    
    hashed_password = make_password(password)
    
    u = user.objects.create(
        email = email,
        password = hashed_password,
        first_name = first_name,
        last_name = last_name,
        phone = phone,
        dateOfBirth = dateOfBirth,
        city = city,
        province = province,
        gender = gender,
    )
    
    serializer = userSerializer(data=request.data)
    
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@parser_classes([JSONParser])
def send_reset_password_email(request):
    email = request.data["email"]
    try:
        user_: user = user.objects.get(email=email)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

    reset = PasswordReset()
    reset.save()
    reset.user = user_
    reset.save()
    try:
        hello = ""
    except:
        return Response(JSONRenderer().render({ "message": "failed to send email" }), 400)
    id = reset._get_pk_val()
    link = f"http://localhost:3000/reset-password?id={id}&email={email}"
    try:
        send_mail(
            "Email de confirmation",
            f"Votre demande de réinitialisation de mot de passe a été approuvée. Veuillez suivre le lien\n {link}\n pour réinitialiser votre mot de passe.",
            "celeq.elhajj@gmail.com",
            [email]
        )
        return Response(JSONRenderer().render({ "message": "email sent" }), 200)
    except:
        return Response(JSONRenderer().render({ "message": "invalid address" }), 400)

@api_view(["PATCH"])
@parser_classes([JSONParser])
def reset_password(request):
    email = request.data["email"]
    reset_id = int(request.data["id"])
    new_password = request.data["newPassword"]
    try:
        reset: PasswordReset = PasswordReset.objects.get(pk=reset_id)
        user_: user = user.objects.get(email=email)
        if user_._get_pk_val() != reset.user_._get_pk_val():
            return Response(JSONRenderer().render({ "message": "failed to reset password" }), 400)
        if user_.check_password(new_password):
            return Response(JSONRenderer().render({ "message": "duplicate password" }), 409)
        user_.set_password(new_password)
        user_.save()
        reset.delete()
        return Response(JSONRenderer().render({ "message": "reset successful" }), 200)
    except:
        return Response(JSONRenderer().render({ "message": "failed to reset password" }), 400)


@api_view(['POST'])
@parser_classes([JSONParser])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        u= authenticate(request, username=email, password=password)

        if u is not None:
            if u.is_email_verified:
                login(request,u)
                return Response({'message': 'Login successful'},status=200)
            else:
                return Response({'message':'email is not verified'},status=400)
            
        else:
            return Response({'error': 'Invalid email or password'}, status=401)
    else:
        return Response({'error': 'Email and password are required'}, status=400)
    

def convert_to_serializable(data):
    """
    Recursively convert non-serializable objects to serializable types.
    """
    if isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, user):
        # Convert CustomUser object to a dictionary of serializable fields
        return {
            'id': data.id,
            'email': data.email,
            # Include other serializable fields of CustomUser
        }
    # Add more conversions as needed
    else:
        # Return the data as is for other types
        return data


   
@csrf_exempt 
def get_user_info(request,email):
    if request.method == 'GET':
            try:
                user_ = get_object_or_404(user,emailUtilisateur=email)
                
                user_info = {
                    'first_name' : user_.first_name,
            'last_name' : user_.last_name,
            'phone' : user_.phone,
            'city' : user_.city,
            'province' : user_.province,
            'gender' : user_.gender,
            'email' : user_.email,
            'dateOfBirth' : user_.dateOfBirth
                }
                user_info = convert_to_serializable(user_info)
                
                return JsonResponse(user_info,content_type = 'application/json')
            
            except user.DoesNotExist:
                return JsonResponse({'error':'user not found'},status=404)
            
    else : 
        return JsonResponse({'error':'methode not allowed'},status=405)
        
        
        
        
        
        
        
    

    
    
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})


@api_view(['GET'])
@parser_classes([JSONParser])
def default(request):
    try:
        send_mail(
            "Welcome",
            "How are you doing",
            "celeq.elhajj@gmail.com",
            ["marzoukayouness@gmail.com"]
        )
        return Response(JSONRenderer().render({ "message": "email sent successfully" }))
    except:
        return Response(JSONRenderer().render({ "message": "failed to send email" }), 400)
    
    

        
        
