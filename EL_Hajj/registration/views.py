from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer , HaajaSerializer
from authentication.models import user 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def registration(request):
    authenticated_user = request.user  
    if request.method == 'GET':
        utilisateur_data = {
            'emailUtilisateur': authenticated_user.email,
            'first_name': authenticated_user.first_name,
            'last_name': authenticated_user.last_name,
            'dateOfBirth': authenticated_user.dateOfBirth,
            'city' : authenticated_user.city,
            'gender' : authenticated_user.gender
        }
        return JsonResponse(utilisateur_data)
    
    elif request.method == 'POST':
        authenticated_user = request.user
        serializer_data = request.data.copy() 
        
        if authenticated_user.gender == 'F':  
            haaja_serializer = HaajaSerializer(data=serializer_data, context={'request': request})
            if haaja_serializer.is_valid():
                haaja_instance = haaja_serializer.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            return Response(haaja_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            haaj_serializer = HaajSerializer(data=serializer_data, context={'request': request})
            if haaj_serializer.is_valid():
                haaj_instance = haaj_serializer.save()
                return Response("Success", status=status.HTTP_201_CREATED)
            return Response(haaj_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    