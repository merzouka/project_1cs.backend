from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer , HaajaSerializer
from authentication.models import user 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from .models import  Baladiya, Tirage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer , HaajaSerializer

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import  Baladiya, Tirage
from authentication.models import user
from django.shortcuts import render

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
        
    




@api_view(['GET'])
@parser_classes([JSONParser])
def baladiya_ids_by_utilisateur(request, utilisateur_id):
    try:
        utilisateur_obj = get_object_or_404(user, id=utilisateur_id)
        baladiya_ids = utilisateur_obj.baladiya_set.values_list('id', flat=True)
        return Response({'baladiya_ids': baladiya_ids}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)





@api_view(['POST'])
@parser_classes([JSONParser])
def associate_tirage_with_baladiyas(request):
    
    utilisateur_id = request.data.get('utilisateur_id')
    type_tirage = request.data.get('type_tirage')
    nombre_de_place = request.data.get('nombre_de_place')

    
    utilisateur_obj = get_object_or_404(user, id=utilisateur_id)

    
    baladiya_ids = utilisateur_obj.baladiya_set.values_list('id', flat=True)

    
    tirage = Tirage.objects.create(
        type_tirage=type_tirage,
        nombre_de_place=nombre_de_place
    )

    
    for baladiya_id in baladiya_ids:
        baladiya = get_object_or_404(Baladiya, id=baladiya_id)
        baladiya.tirage = tirage
        baladiya.save()

 
    return Response({'message': 'Tirage information associated with Baladiyas successfully'}, status=201)


def index(request):
    return render(request, 'test2.html')