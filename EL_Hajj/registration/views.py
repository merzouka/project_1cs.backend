import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaajSerializer 
from authentication.models import user 
from rest_framework.permissions import IsAuthenticated
from .models import  Baladiya, Tirage, Haaj, Winners
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
import random 







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
        if authenticated_user.winner:
            last_winning_date = authenticated_user.winning_date
            ten_years_ago = datetime.now() - datetime.timedelta(days=365 * 10)
            if last_winning_date > ten_years_ago:
                return Response("You cannot register for the draw as you have won in the last 10 years.", status=status.HTTP_400_BAD_REQUEST)
        
        serializer_data = request.data.copy() 
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
    tranche_age = request.data.get('tranche_age')
    
    utilisateur_obj = get_object_or_404(user, id=utilisateur_id)

    
    baladiya_ids = utilisateur_obj.baladiya_set.values_list('id', flat=True)

    
    tirage = Tirage.objects.create(
        type_tirage=type_tirage,
        nombre_de_place=nombre_de_place,
        tranche_age=tranche_age 
    )

    
    for baladiya_id in baladiya_ids:
        baladiya = get_object_or_404(Baladiya, id=baladiya_id)
        baladiya.tirage = tirage
        baladiya.save()

 
    return Response({'message': 'Tirage information associated with Baladiyas successfully'}, status=201)



@api_view(['GET'])
def fetch_winners(request, id_utilisateur):
    try:
        user_instance = get_object_or_404(user, id=id_utilisateur)
        baladiyas_in_group = Baladiya.objects.filter(id_utilisateur=user_instance)
        baladiya_names = [baladiya.name for baladiya in baladiyas_in_group]
        first_baladiya = Baladiya.objects.filter(id_utilisateur=id_utilisateur).first()

        condidats = []

        for baladiya_name in baladiya_names:
            haajs_in_city = Haaj.objects.filter(user__city=baladiya_name)
            haajas_in_city = Haaja.objects.filter(user__city=baladiya_name)
            condidats.extend(haajs_in_city)
            condidats.extend(haajas_in_city)

        id_tirage = first_baladiya.tirage.id
        number_of_winners_needed = Tirage.objects.get(id=id_tirage).nombre_de_place
        type_de_tirage = Tirage.objects.get(id=id_tirage).type_tirage

        selected_winners = []

        if type_de_tirage == 1:
            while len(selected_winners) < number_of_winners_needed:
                selected_condidat = random.choice(condidats)
                if selected_condidat.user.gender == 'M':
                    selected_winners.append(selected_condidat.user.id)
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                    
                elif selected_condidat.user.gender == 'F':
                    selected_winners.append(selected_condidat.user.id)
                    condidats.remove(selected_condidat)
                    Winners.objects.create(nin=selected_condidat.user.id)
                    maahram_instance = user.objects.get(id=selected_condidat.maahram_id)
                    selected_winners.append(maahram_instance.id)
                    Winners.objects.create(nin=maahram_instance.id)
                    
        return Response({'winners': selected_winners}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
